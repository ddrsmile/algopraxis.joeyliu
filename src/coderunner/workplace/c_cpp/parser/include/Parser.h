#include "BaseParser.h"

#ifndef INTEGERPARSER_H
#define INTEGERPARSER_H

using namespace std;

class IntegerParser: public BaseParser<int> {
    public:
        IntegerParser() = default;
        virtual ~IntegerParser() = default;

        static void* create() {
            IParser<int>* obj = new IntegerParser();
            return obj;
        }

    protected:
        int toValue(string& str);
};

inline int IntegerParser::toValue(string& str) {
    return stoi(str);
}

class DoubleParser: public BaseParser<double> {
    public:
        DoubleParser() = default;
        virtual ~DoubleParser() = default;

        static void* create() {
            IParser<double>* obj = new DoubleParser();
            return obj;
        }

    protected:
        double toValue(string& str);
};
inline double DoubleParser::toValue(string& str) {
    return stod(str);
}

class StringParser: public BaseParser<string> {
    public:
        StringParser() = default;
        virtual ~StringParser() = default;

        static void* create() {
            IParser<string>* obj = new StringParser();
            return obj;
        }

    protected:
        string toValue(string& str);
};
inline string StringParser::toValue(string& str) {
    return h::trim(str);
}
#endif