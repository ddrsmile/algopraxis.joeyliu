#include <vector>
#include <memory>

using namespace std;

#ifndef IPARSER_H
#define IPARSER_H

template <class E>
class IParser {
    public:
        IParser() = default;
        virtual ~IParser() = default;
        virtual void free() = 0;
        virtual void set_input_path(const string& input_path) = 0;

        virtual vector<E> parseDataAsSingleValue() = 0;
        virtual vector<vector<E>> parseDataAsList() = 0;
        virtual vector<vector<vector<E>>> parseDataAsLists() = 0;

};
#endif