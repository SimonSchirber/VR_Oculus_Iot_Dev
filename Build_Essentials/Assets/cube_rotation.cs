using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cube_rotation : MonoBehaviour
{
    // Start is called before the first frame update
    private float angle_per_frame = 0.05f;


    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        transform.Rotate(0, angle_per_frame, 0, Space.Self);//x,y,z
    }
}
