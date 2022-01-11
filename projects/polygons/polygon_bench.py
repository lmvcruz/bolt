from pathlib import Path

from bolt import Parameter
from bolt.engine import Engine
from bolt.program import ExternalProgram


def generate_polygons():
    polygon_folder = Path(".").joinpath("projects", "polygons")
    prog_path = polygon_folder.joinpath(
        "polygons_generation", "build", "generate_polygons"
    ).absolute()
    data_folder = polygon_folder.joinpath("data")

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


def main():
    generate_polygons()


if __name__ == "__main__":
    main()
