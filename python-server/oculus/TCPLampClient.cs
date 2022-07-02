using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading;
using UnityEngine;

public class TCPLampClient : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField] private string serverIP = "147.182.239.226";
    [SerializeField] private int serverPORT = 33333;

    void Start()
    {
        
        
    }

    public void get_state()
    {
        ConnectClient(serverIP,serverPORT,1,"lamp1:state");
    }

    private void ConnectClient(string server, int port, int clientID, string payload)
    {
        try
        {
            TcpClient client = new TcpClient(server,port);
            NetworkStream stream = client.GetStream();

            if(client.Connected)
            {
                Debug.Log("client connected");
                byte[] bytes = System.Text.Encoding.ASCII.GetBytes(payload);
                stream.Write(bytes,0,bytes.Length);

                byte[] data = new byte[256];
                int data_bytes = stream.Read(data,0,data.Length);
                string response = System.Text.Encoding.ASCII.GetString(data,0,data_bytes);
                Debug.Log(response);
            }
            stream.Close();
            client.Close();
        }
        catch(System.Exception e)
        {

        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
