var Pager = function (obj) {
    var page, str, max, start, i, totalCount = parseInt(obj.totalCount || 0), pageSize = parseInt(obj.pageSize || 10),
        buttonSize = parseInt(obj.buttonSize || 10), pageParam = obj.pageParam || "page",
        className = obj.className || "pagination", prevButton = obj.prevButton || "&laquo;",
        nextButton = obj.nextButton || "&raquo;", firstButton = obj.firstButton || "",
        lastButton = obj.lastButton || "";
    if (Pager.getParam = function (a) {
        var b = new RegExp("(^|&)" + a + "=([^&]*)(&|$)", "i"), c = window.location.search.substr(1).match(b);
        return null != c ? unescape(c[2]) : null
    }, Pager.replaceUrl = function (name, value) {
        var oUrl = window.location.href, reg = new RegExp("(^|&)(" + name + "=)([^&]*)(&|$)", "i"),
            r = window.location.search.substr(1).match(reg);
        return null != r ? oUrl.replace(eval("/" + r[0] + "/g"), r[1] + r[2] + value + r[4]) : oUrl + (oUrl.indexOf("?") > 0 ? "&" : "?") + name + "=" + value
    }, 0 == totalCount || pageSize >= totalCount) return "";
    for (page = parseInt(Pager.getParam(pageParam)) || 0, page = page > 1 ? page : 1, str = '<ul class="' + className + '">', firstButton && (str += '<li class="prev"><a href="' + Pager.replaceUrl(pageParam, 1) + '">' + firstButton + "</a></li>"), str += 1 >= page ? '<li class="prev disabled"><span>' + prevButton + "</span></li>" : '<li class="prev"><a href="' + Pager.replaceUrl(pageParam, page - 1) + '">' + prevButton + "</a></li>", max = Math.ceil(totalCount / pageSize), start = Math.floor((page - 2) / (buttonSize - 2)) * (buttonSize - 2), start = start + buttonSize > max ? max - buttonSize : start, start = start >= 0 ? start : 0, i = start + 1; start + buttonSize >= i && !(i > max || 3 > buttonSize); i++) str += "<li" + (i == page ? ' class="active"' : "") + '><a href="' + Pager.replaceUrl(pageParam, i) + '">' + i + "</a></li>";
    return str += page >= max ? '<li class="next disabled"><span>' + nextButton + "</span></li>" : '<li class="next"><a href="' + Pager.replaceUrl(pageParam, page + 1) + '">' + nextButton + "</a></li>", lastButton && (str += '<li class="next"><a href="' + Pager.replaceUrl(pageParam, max) + '">' + lastButton + "</a></li>"), str + "</ul>"
};