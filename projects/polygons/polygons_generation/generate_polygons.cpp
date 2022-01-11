#include <cmath>
#include <iostream>
#include <random>
#include <string>

#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

const float Pi = 3.14159265359;

enum PolygonType : int
{
    Square = 1,
    Triangle = 2,
    Circle = 3
};

// PolygonType num2polygontype(int num)
// {
//     return PolygonType(num);
// }

std::string polygon2string(const PolygonType &pt)
{
    switch (pt)
    {
    case Square:
        return "Square";
        break;
    case Triangle:
        return "Triangle";
        break;
    case Circle:
        return "Circle";
        break;
    }
    return "Error";
}

int random_integer(int min_v, int max_v)
{
    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> uni(min_v, max_v);
    return uni(rng);
}

cv::Point internalRandomPoint(cv::Mat &img, int ray)
{
    int offset = 2;
    int cx = random_integer(ray + offset, img.cols - offset - ray);
    int cy = random_integer(ray + offset, img.rows - offset - ray);
    return cv::Point(cx, cy);
}

void drawCircle(cv::Mat &img, int ray)
{
    cv::Point center = internalRandomPoint(img, ray);
    cv::circle(img,
               center,
               ray,
               cv::Scalar(0, 0, 255),
               cv::FILLED,
               cv::LINE_8);
}

void drawSquare(cv::Mat &img, int length)
{
    int half = length / 2;
    cv::Point center = internalRandomPoint(img, length);
    cv::Point topLeftPoint(center.x - half, center.y - half);
    cv::Point bottomRightPoint(center.x + half, center.y + half);
    cv::rectangle(img,
                  topLeftPoint,
                  bottomRightPoint,
                  cv::Scalar(0, 0, 255),
                  cv::FILLED,
                  cv::LINE_8);
}

void drawTriangle(cv::Mat &img, int ray)
{
    cv::Point center = internalRandomPoint(img, ray);
    std::vector<std::vector<cv::Point>> triangles(1);
    triangles[0].resize(3);

    for (int i = 0; i < 3; i++)
    {
        float angle = (-90.0f + i * 120.0f) * Pi / 180.0f;
        triangles[0][i] = cv::Point(center.x + (ray * std::cos(angle)), center.y + (ray * std::sin(angle)));
    }

    cv::fillPoly(img,
                 triangles,
                 cv::Scalar(0, 0, 255),
                 cv::LINE_8);
}

void create_image(std::string filename, int w, int h, int polSize, PolygonType &pt)
{
    cv::Mat img(h, w, CV_8UC3);
    img = cv::Scalar(255, 255, 255);

    switch (pt)
    {
    case Square:
        drawSquare(img, polSize);
        break;
    case Triangle:
        drawTriangle(img, polSize);
        break;
    case Circle:
        drawCircle(img, polSize);
        break;
    default:
        break;
    }
    cv::imwrite(filename, img);
}

int main(int argc, char *argv[])
{
    int imgWidth = std::stoi(argv[1]);
    int imgHeight = std::stoi(argv[2]);

    auto polygonsType = PolygonType(std::stoi(argv[3]));
    std::string filename = argv[4];
    int polSize = std::min(imgWidth, imgHeight) / 10;
    std::cout << polygon2string(polygonsType) << ": " << polSize << std::endl;
    create_image(filename, imgWidth, imgHeight, polSize, polygonsType);
    return 0;
}
