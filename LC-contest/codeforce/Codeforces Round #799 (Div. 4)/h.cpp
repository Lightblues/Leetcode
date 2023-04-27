#include "bits/stdc++.h"
using namespace std;
 
#define ll long long
 
#define       forn(i,n)              for(int i=0;i<n;i++)
#define          all(v)              v.begin(), v.end()
#define         rall(v)              v.rbegin(),v.rend()
 
#define            pb                push_back
#define          sz(a)               (int)a.size()
 
struct DynamicMaxSubarraySum {
    struct node {
        ll pref, suf, val, sum;
    };  
    int N;
    ll neutral;
    vector<node> t;
    DynamicMaxSubarraySum(int _N, ll assign_value) {
        neutral = assign_value;
        N = _N;
        t.resize(4 * N);
        forn(i, 4 * N) t[i] = {0, 0, 0, 0};
        build(1, 0, N - 1); 
    }
    void build(int i, int l, int r) {
        if(l == r) {
            t[i].pref = t[i].suf = t[i].val = t[i].sum = neutral;
            return;
        }
        int mid = (l + r) >> 1;
        build(2 * i, l, mid);
        build(2 * i + 1, mid + 1, r);
        t[i] = merge(t[2 * i], t[2 * i + 1]);
    }
    node merge(node a, node b) {
        node c;
        c.pref = max(a.pref, a.sum + b.pref);
        c.suf = max(b.suf, b.sum + a.suf);
        c.val = max({a.val, b.val, a.suf + b.pref});
        c.sum = a.sum + b.sum;
        return c;
    }
 
    void modif(int i, int l, int r, int pos, ll val) {
        if(l > pos || r < pos) return;
        if(l == pos && r == pos) {
            t[i].pref = t[i].suf = t[i].val = t[i].sum = val;
            return;
        }
        int mid = (l + r) >> 1;
        modif(2 * i, l, mid, pos, val);
        modif(2 * i + 1, mid + 1, r, pos, val);
        t[i] = merge(t[2 * i], t[2 * i + 1]);
    }
    node query(int i, int l, int r, int tl, int tr) {
        if(l > tr || r < tl) return {0, 0, 0, 0};
        if(l >= tl && r <= tr) return t[i];
        int mid = (l + r) >> 1;
        return merge(query(2 * i, l, mid, tl, tr), query(2 * i + 1, mid + 1, r, tl, tr));
    }
 
    void modif(int pos, int val) {
        modif(1, 0, N - 1, pos, val);
    }
    node query(int l, int r) {
        return query(1, 0, N - 1, l, r);
    }
    node query(int pos) {
        return query(1, 0, N - 1, pos, pos);
    }
};
 
void solve() {  
    int n; cin >> n;
    vector<int> a(n);
    forn(i, n) cin >> a[i];
    map<int, vector<int>> vv;
    forn(i, n) {
        vv[a[i]].pb(i);
    }
    DynamicMaxSubarraySum st(n, -1);
 
    ll mx = 0, ans = -1;
    for(auto i: vv) {
        vector<int> v = i.second;
        for(auto x: v) st.modif(x, 1);
        if(mx < st.query(0, n - 1).val) {
            ans = i.first;
            mx = st.query(0, n - 1).val;
        }
        for(auto x: v) st.modif(x, -1);
    }  
    int ansl = -1, ansr = -1;
    for(int i = 0; i < n; ++i) {
        if(a[i] == ans) a[i] = 1;
        else a[i] = -1;
    }
    ll sum = 0, lastl = 0;
    mx = 0;
    for(int i = 0; i < n; ++i) {
        sum += a[i];
        if(sum > mx) {
            mx = sum;
            ansr = i;
            ansl = lastl;
        }
        if(sum <= 0) {
            lastl = i + 1;
            sum = 0;
        }
    }
 
    cout << ans << " " << ansl + 1 << " " << ansr + 1 << "\n"; 
}   
     
int32_t main() {
    ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);
    int t = 1;
    cin >> t;
    while(t--) {
        solve();
    }
}
