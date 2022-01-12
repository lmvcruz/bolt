import shutil

from pathlib import Path

from bolt import Parameter
from bolt.engine import Engine
from bolt.program import ExternalProgram, Program


class FileMoveProgram(Program):
    """This class is a post-processing applied over the engine report

       It moves the files in input argument to the respective folder according
       to the classification (result of classification program execution)
    """

    def __init__(self, data_folder: Path) -> None:
        super().__init__(FileMoveProgram.__name__)
        self.triangles_folder = data_folder.joinpath("triangles")
        self.squares_folder = data_folder.joinpath("squares")
        self.circles_folder = data_folder.joinpath("circles")
        self.errors_folder = data_folder.joinpath("errors")

        self.triangles_folder.mkdir(exist_ok=True)
        self.squares_folder.mkdir(exist_ok=True)
        self.circles_folder.mkdir(exist_ok=True)
        self.errors_folder.mkdir(exist_ok=True)

    def run(self, par: Parameter):
        filename = par["input"]["arguments"][0]
        result = par["output"]["result"].split("\n")[0]
        file_dest = self.__get_result_folder(result).joinpath(Path(filename).name)
        print(str(file_dest.absolute()), filename)
        shutil.move(src=filename, dst=str(file_dest.absolute()))

    def __get_result_folder(self, result):
        if result == "Triangle":
            return self.triangles_folder
        if result == "Square":
            return self.squares_folder
        if result == "Circle":
            return self.circles_folder
        return self.errors_folder


def generate_polygons():
    file_folder = Path(__file__).parent.absolute()
    prog_path = file_folder.joinpath(
        "polygons_generation", "build", "generate_polygons"
    ).absolute()
    data_folder = file_folder.joinpath("data")

    engine = Engine()
    engine.add_program(ExternalProgram("PolygonsGeneration", prog_path))
    polygon_quantities = {1: 5, 2: 6, 3: 3}
    img_counter = 0
    img_width = 300
    img_height = 200
    for (poly, qty) in polygon_quantities.items():
        for _ in range(qty):
            img_counter += 1
            filename = data_folder.joinpath(f"img_{img_counter}.png").absolute()
            par = Parameter(
                {
                    "arguments": [
                        str(img_width),
                        str(img_height),
                        str(poly),
                        str(filename),
                    ]
                }
            )
            engine.add_input(par)
    engine.run()
    engine.report.show()


def classify_image():
    print("Classify")
    file_folder = Path(__file__).parent.absolute()
    prog_path = file_folder.joinpath(
        "polygons_classification", "build", "classify_polygons"
    ).absolute()
    data_folder = file_folder.joinpath("data")

    engine = Engine()
    engine.add_program(ExternalProgram("PolygonsClassification", prog_path))

    for img_name in data_folder.iterdir():
        if img_name.suffix != ".png":
            continue
        par = Parameter({"arguments": [str(img_name)]})
        engine.add_input(par)
    engine.run()
    engine.post_processing(FileMoveProgram(data_folder))


def main():
    # This benchmark project performs two massive executions:
    # File generations: images containing a circle, square or triangle
    # File Classification and Moving: the classification is performed using an
    #       external program (C++) and the moving is a post-processing execution
    #       based on the classification in the report
    #
    # This project illustrates (i) how to use bolt in a project for massive
    # processing execution, (ii) how to use external programs and (iii) how to
    # perform post-processing based in the engine report
    generate_polygons()
    classify_image()


if __name__ == "__main__":
    main()
