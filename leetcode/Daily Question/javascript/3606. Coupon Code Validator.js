/*
https://leetcode.com/problems/coupon-code-validator/description/

Автор: Дуплей Максим Игоревич
ORCID: https://orcid.org/0009-0007-7605-539X
GitHub: https://github.com/QuadDarv1ne/
*/

var validateCoupons = function(code, businessLine, isActive) {
    /*
    Решение задачи Coupon Code Validator (LeetCode 3606).

    Идея:
    - Фильтруем по правилам:
      активность, допустимые бизнес‑линии, код не пустой и только [A‑Za‑z0‑9_].
    - Затем сортируем по порядку businessLine и внутри – по коду.
    */
    const order = ["electronics","grocery","pharmacy","restaurant"];
    const pattern = /^[A-Za-z0-9_]+$/;

    let valid = [];
    for (let i = 0; i < code.length; i++) {
        if (isActive[i] &&
            order.includes(businessLine[i]) &&
            code[i].length > 0 &&
            pattern.test(code[i])) {
            valid.push({bl: businessLine[i], c: code[i]});
        }
    }

    valid.sort((a,b) => {
        if (a.bl === b.bl) return a.c.localeCompare(b.c);
        return order.indexOf(a.bl) - order.indexOf(b.bl);
    });

    return valid.map(x => x.c);
};
