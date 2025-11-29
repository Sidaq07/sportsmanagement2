#include <iostream>
#include <climits>
using namespace std;

int main()
{
    int n;
    cout << "Enter number of nodes in graph ";
    cin >> n;
    int A[n][n]; 
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = 0;

    int E;
    cout << "Enter number of edges ";
    cin >> E;

    cout << "Enter edges as: start end forward_capacity backward_capacity\n";
    for (int i = 0; i < E; i++)
    {
        int s, e, w1, w2;
        cin >> s >> e >> w1 >> w2;
        A[s][e] = w1;
        A[e][s] = w2;

    int source, sink;
    cout << "Enter source " ;
    cin >> source;
    cout << "Enter sink "<<endl;
    cin >> sink;

    int maxFlow = 0;
    while (true)
    {
        
        int Queue[n], parent[n], status[n];
        int f = 0, r = 0;

        for (int i = 0; i < n; i++)
        {
            parent[i] = -1;
            status[i] = 1;
        }

        Queue[r++] = source;
        status[source] = 2; 
        bool found = false;

        while (f < r && !found)
        {
            int v = Queue[f++];
            status[v] = 3;
            for (int i = 0; i < n; i++)
            {
                if (A[v][i] > 0 && status[i] == 1)
                {
                    Queue[r++] = i;
                    parent[i] = v;
                    status[i] = 2;
                    if (i == sink)
                    {
                        found = true;
                        break;
                    }
                }
            }
        }

        if (!found)
            break;

        int pathFlow = 0;
        int v = sink;
        while (v != source)
        {
            int u = parent[v];
            pathFlow = min(pathFlow, A[u][v]);
            v = u;
        }

        
        v = sink;
        while (v != source)
        {
            int u = parent[v];
            A[u][v]-=pathFlow;
            A[v][u]+=pathFlow;
        }
        maxFlow+=pathFlow;
    }


    return 0;
}
}