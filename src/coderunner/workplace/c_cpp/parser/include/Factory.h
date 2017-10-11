#include <string>
#include <unordered_map>
#include "Parser.h"

using namespace std;

#ifndef FACTORY_H
#define FACTORY_H

class Factory {

    typedef void* (*CreateObjFn)();
    typedef unordered_map<string, CreateObjFn> registry_map;

    public:
        Factory();

	    template <class T>
	    IParser<T>* create(const string& name);

    private:
        registry_map registered_map;

        void Register(const string& name, CreateObjFn pCreateFn);
};

#endif