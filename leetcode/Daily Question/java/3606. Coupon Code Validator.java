/*
https://leetcode.com/problems/coupon-code-validator/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

import java.util.*;
import java.util.regex.Pattern;

class Solution {
    public List<String> validateCoupons(String[] code, String[] businessLine, boolean[] isActive) {
        String[] order = {"electronics","grocery","pharmacy","restaurant"};
        Map<String,Integer> pos = new HashMap<>();
        for (int i=0;i<order.length;i++) pos.put(order[i], i);

        Pattern pattern = Pattern.compile("^[A-Za-z0-9_]+$");
        List<int[]> idxs = new ArrayList<>();
        List<String> validCodes = new ArrayList<>();

        for (int i=0; i<code.length; i++) {
            if (isActive[i] && pos.containsKey(businessLine[i]) && code[i].length()>0 && pattern.matcher(code[i]).matches()) {
                validCodes.add(code[i]);
                idxs.add(new int[]{pos.get(businessLine[i]), validCodes.size()-1});
            }
        }

        // Сортировка по категории и затем по строке
        Collections.sort(idxs, (a,b) -> {
            int da = a[0], db = b[0];
            if (da == db) return validCodes.get(a[1]).compareTo(validCodes.get(b[1]));
            return da - db;
        });

        List<String> answer = new ArrayList<>();
        for (int[] p : idxs) answer.add(validCodes.get(p[1]));
        return answer;
    }
}
