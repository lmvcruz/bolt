#include <iostream>

#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

#include <vector>

using Contour = std::vector<cv::Point>;
using ContoursHierarchy = std::vector<Contour>;

cv::Mat binarizeImage(cv::Mat &image)
{
    cv::Mat img_gray;
    cvtColor(image, img_gray, cv::COLOR_BGR2GRAY);

    cv::Mat binary;
    cv::threshold(img_gray, binary, 150, 255, cv::THRESH_BINARY);

    return binary;
}

ContoursHierarchy detectCountours(cv::Mat &image)
{
    cv::Mat binary = binarizeImage(image);

    ContoursHierarchy contours;
    std::vector<cv::Vec4i> hierarchy;

    findContours(binary, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_NONE);

    for (size_t k = 0; k < contours.size(); k++)
        approxPolyDP(cv::Mat(contours[k]), contours[k], 3, true);

    return contours;
}

void classifyContour(Contour &contour)
{
    if (contour.size() == 3)
        std::cout << "Triangle" << std::endl;
    else if (contour.size() == 4)
        std::cout << "Square" << std::endl;
    else
        std::cout << "Circle" << std::endl;
}

void classify_image(cv::Mat &image)
{
    auto contours = detectCountours(image);
    for (size_t k = 0; k < contours.size(); k++)
    {
        if (cv::contourArea(contours[k]) > image.rows * image.cols * 0.9)
            continue;
        classifyContour(contours[k]);
    }
}

int main(int argc, char *argv[])
{
    std::string filename = argv[1];
    cv::Mat mat = cv::imread(filename);
    // std::cout << "Counting: " << mat.rows << " " << mat.cols << std::endl;
    classify_image(mat);
    return 0;
}