""" 
合并区间
"""

def getMergedIntervals(intervals):
    intervals.sort()
    ans = []
    ll,rr = intervals[0]
    for l,r in intervals[1:]:
        if l<=rr:
            rr = max(rr,r)
        else:
            ans.append([ll,rr])
            ll,rr = l,r
    ans.append([ll,rr])
    return ans

print(
    getMergedIntervals([[4,8],[2,6],[5,7]]), 
)
