#include <vector>
#include <string>
#include <sstream>

#ifndef PARSER_HELPERS_H
#define PARSER_HELPERS_H

namespace {
    namespace h {
        inline vector<string> split(const string& str, char delim) {
            stringstream ss(str);
            string token;
            vector<string> tokens;
            while (getline(ss, token, delim)) {
                tokens.push_back(token);
            }
            return tokens;
        }

        inline vector<string> split(const string& str, const string& delim) {
            string::size_type pos = 0;
            string resource = str;
            string token;
            vector<string> tokens;
            while ((pos = resource.find(delim)) != string::npos) {
                token = resource.substr(0, pos);
                tokens.push_back(token);
                resource.erase(0, pos + delim.length());
            }
            tokens.push_back(resource);
            return tokens;
        }

        inline string remove_space(const string& str) {
            string output = str;
            output.erase(remove_if(output.begin(),output.end(), [](char x){return isspace(x);}),output.end());
            return output;
        }

        inline string find_and_replace(const string& str, const string& find, const string& replace) {
            string::size_type pos = 0;
            string output = str;
            while ((pos = output.find(find, pos) != string::npos)) {
                output.replace(pos, find.length(), replace);
                pos += replace.length();
            }
            return output;
        }

        inline string trim(const string& str) {
            string output = str;
            if (!output.empty()) {
                output.erase(0, output.find_first_not_of(" "));
                output.erase(output.find_last_not_of(" ") + 1);
            }
            return output;
        }
    } //namespace h
} // namespace

#endif