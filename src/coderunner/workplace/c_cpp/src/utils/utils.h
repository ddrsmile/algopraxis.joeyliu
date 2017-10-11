#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iterator>

using namespace std;

#ifndef UTILS_H
#define UTILS_H

// overload << operator to show vectors
template<typename T>
ostream& operator<< (ostream& out, const vector<T>& v) {
    if (!v.empty()) {
        out << "[";
        copy (v.begin(), v.end() - 1, ostream_iterator<T>(out, ", "));
        out << v.back();
        out << "]";
    } else {
        out << "[]";
    }
    return out;
}

// parse commandline input
string GetFilePath(int argc, char* argv[]) {
    string path;
    if (argc == 2) {
        path = argv[1];
    } else {
        path = "";
    }
    return path;
}

#endif

