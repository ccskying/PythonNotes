# short clear solution. But not fast
class Solution:
    def licenseKeyFormatting(self, s: str, k: int) -> str:
        s = s.replace("-","").upper()
        res = ""
        while s:
            res = s[-k:] + res
            s = s[:-k]
            if s : res = "-" + res
        return res