#include <iostream>

#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

int main()
{
    cv::Mat mat = cv::imread("../../data/test.png");
    std::cout << "Counting: " << mat.rows << " " << mat.cols << std::endl;
    return 0;
}