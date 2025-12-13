/*
https://leetcode.com/problems/coupon-code-validator/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

using System.Text.RegularExpressions;

public class Solution {
    public IList<string> ValidateCoupons(string[] code, string[] businessLine, bool[] isActive) {
        string[] order = {"electronics","grocery","pharmacy","restaurant"};
        Dictionary<string,int> pos = new Dictionary<string,int>();
        for (int i=0;i<order.Length;i++) pos[order[i]] = i;

        Regex pattern = new Regex(@"^[A-Za-z0-9_]+$");
        var list = new List<(int,string)>();

        for (int i=0;i<code.Length;i++) {
            if (isActive[i] && pos.ContainsKey(businessLine[i]) && !string.IsNullOrEmpty(code[i]) && pattern.IsMatch(code[i])) {
                list.Add((pos[businessLine[i]], code[i]));
            }
        }

        list.Sort((a,b) => {
            if (a.Item1 == b.Item1) return a.Item2.CompareTo(b.Item2);
            return a.Item1.CompareTo(b.Item1);
        });

        var result = new List<string>();
        foreach (var x in list) result.Add(x.Item2);
        return result;
    }
}
