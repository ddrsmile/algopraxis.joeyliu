#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <memory>

#include "IParser.h"
#include "helpers.h"
using namespace std;

#ifndef BASEPARSER_H
#define BASEPARSER_H

template <class E>
class BaseParser : public virtual IParser<E> {
    public:
        BaseParser() = default;
        virtual ~BaseParser() = default;
        void free();
        void set_input_path(const string& input_path);

        vector<E> parseDataAsSingleValue();
        vector<vector<E>> parseDataAsList();
        vector<vector<vector<E>>> parseDataAsLists();

    protected:
        string input_path_;
        virtual E toValue(string& str) = 0;
        vector<E> toList(string& str);
        vector<vector<E>> toLists(string& str);
};

template <class E>
void BaseParser<E>::free() {
    delete this;
}

template <class E>
void BaseParser<E>::set_input_path(const string& input_path) {
    this->input_path_ = input_path;
}

template <class E>
inline
vector<E> BaseParser<E>::toList(string& str) {
    vector<E> output;
    if (str[0] != '[' && str[str.size() - 1] != ']') {
        output.push_back(this->toValue(str));
    }

    str = str.substr(1, str.size() - 2);
    if (str.size() == 0) return output;
    str = h::remove_space(str);
    vector<string> input_contents = h::split(str, ',');
    for (vector<string>::iterator it = input_contents.begin(); it != input_contents.end(); it++) {
        output.push_back(this->toValue(*it));
    }
    return output;
}

template <class E>
inline
vector<vector<E>> BaseParser<E>::toLists(string& str) {
    vector<vector<E>> output;
    if (str[0] != '[' && str[str.size() - 1] != ']') {
        output.push_back(this->toList(str));
    }

    str = str.substr(1, str.size() - 2);
    if (str.size() == 0) return output;
    str = h::remove_space(str);
    str = h::find_and_replace(str, "],[", "], [");
    vector<string> input_contents = h::split(str, ", ");
    for (vector<string>::iterator it = input_contents.begin(); it != input_contents.end(); it++) {
        output.push_back(this->toList(*it));
    }
    return output;
}

template <class E>
vector<E> BaseParser<E>::parseDataAsSingleValue() {
    vector<E> output;
    if (this->input_path_.size() == 0) {
        return output;
    }
    string str;
    ifstream input_contents(this->input_path_);
    while (getline(input_contents, str)) {
        output.push_back(this->toValue(str));
    }
    return output;
}

template <class E>
inline
vector<vector<E>> BaseParser<E>::parseDataAsList() {
    vector<vector<E>> output;
    if (this->input_path_.size() == 0) {
        return output;
    }
    string str;
    ifstream input_contents(this->input_path_);
    while (getline(input_contents, str)) {
        output.push_back(this->toList(str));
    }
    return output;
}

template <class E>
inline
vector<vector<vector<E>>> BaseParser<E>::parseDataAsLists() {
    vector<vector<vector<E>>> output;
    if (this->input_path_.size() == 0) {
        return output;
    }
    string str;
    ifstream input_contents(this->input_path_);
    while (getline(input_contents, str)) {
        output.push_back(this->toLists(str));
    }
    return output;
}
#endif