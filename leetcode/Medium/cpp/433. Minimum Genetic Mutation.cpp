/**
 * https://leetcode.com/problems/minimum-genetic-mutation/description/?envType=study-plan-v2&envId=top-interview-150
 */

#include <string>
#include <vector>
#include <queue>
#include <unordered_set>

using namespace std;

class Solution {
public:
    int minMutation(string startGene, string endGene, vector<string>& bank) {
        unordered_set<string> bankSet(bank.begin(), bank.end());
        if (bankSet.find(endGene) == bankSet.end()) {
            return -1;
        }

        queue<pair<string, int>> q;
        q.push({startGene, 0});

        while (!q.empty()) {
            auto [gene, level] = q.front();
            q.pop();

            for (int i = 0; i < (int)gene.size(); ++i) {
                char original = gene[i];
                for (char c : {'A', 'C', 'G', 'T'}) {
                    gene[i] = c;
                    if (gene == endGene) {
                        return level + 1;
                    }
                    if (bankSet.find(gene) != bankSet.end()) {
                        bankSet.erase(gene);
                        q.push({gene, level + 1});
                    }
                }
                gene[i] = original;
            }
        }

        return -1;
    }
};

/*
''' Полезные ссылки: '''
# 1. 💠Telegram💠❃ Хижина программиста Æ: https://t.me/hut_programmer_07
# 2. 💠Telegram №1💠 @quadd4rv1n7
# 3. 💠Telegram №2💠 @dupley_maxim_1999
# 4. Rutube канал: https://rutube.ru/channel/4218729/
# 5. Plvideo канал: https://plvideo.ru/channel/AUPv_p1r5AQJ
# 6. YouTube канал: https://www.youtube.com/@it-coders
# 7. ВК группа: https://vk.com/science_geeks
*/