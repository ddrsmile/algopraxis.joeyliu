#include <memory>
#include "Factory.h"
#include "main.h"
#include "sols.cpp"

int main(int argc, char* argv[]) {
    string path = GetFilePath(argc, argv);
    Factory factory;
    unique_ptr<IParser<int>> integerParser(factory.create<int>("integer"));


    integerParser->set_input_path(path);
    Solution sol = Solution();

    vector<vector<int>> inIntVector = integerParser->parseDataAsList();
    for (int i = 0; i < inIntVector.size()/2; i++) {
        vector<int> nums = inIntVector[2*i];
        int target = inIntVector[2*i + 1][0];
        vector<int> res = sol.twoSum(nums, target);
        cout << res << endl;
    }

    integerParser = NULL;

    return 0;
}
