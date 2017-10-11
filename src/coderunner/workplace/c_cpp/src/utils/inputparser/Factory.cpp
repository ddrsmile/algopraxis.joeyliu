#include "Factory.h"

Factory::Factory() {
    Register("integer", &IntegerParser::create);
    Register("double", &DoubleParser::create);
    Register("string", &StringParser::create);
}

template <class T>
IParser<T>* Factory::create(const string& name) {
    registry_map::iterator it = registered_map.find(name);
    if (it != registered_map.end()) {
        void* pObj = it->second();
        IParser<T>* obj = static_cast<IParser<T>*>(pObj);
        return obj;
    }
    throw "Factory::create: key was not found in hash map.  Did you forget to register it?";
}

void Factory::Register(const string& name, CreateObjFn pCreateFn) {
    registered_map[name] = pCreateFn;
}