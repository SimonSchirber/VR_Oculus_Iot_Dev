using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Oculus.Interaction.Input;

public class touch_change : MonoBehaviour
{
    private float angle_per_frame = 0.05f;
    [SerializeField] private GameObject dirtblock;
    [SerializeField] private Transform fingertip;
    [SerializeField] private AudioSource dig;
    [SerializeField] private float distance_threshold = .05f; //.05 = 5cm
    // Start is called before the first frame update
    private bool isHit = false;
    private bool wasHit = false;
    private bool isEnter = false;
    private bool isExit = false;
    private float distance = Mathf.Infinity;
    private float touch_threshold;
    
   

    // Update is called once per frame
    void Update()
    {
        distance = DistanceCalculator(dirtblock, fingertip);
        touch_threshold = distance_threshold + 0.5f*dirtblock.transform.localScale.y;//since square doesn't matter which axis
        isHit = (distance < touch_threshold);
        isEnter = isHit && !wasHit;
        isExit = !isHit && wasHit;

        if (isEnter){
            dig.Play();
        }
        if (isExit){
            dig.Play();
            ChangeColor(dirtblock);
        }
        wasHit = isHit;
        
    }

    private void ChangeColor(GameObject dirtblock){
        var cuberender = dirtblock.GetComponent<Renderer>();
        // set color
        Color newcolor = new Color(Random.value,Random.value, Random.value, 1.0f);
        cuberender.material.SetColor("_Color", newcolor);
    }

    private float DistanceCalculator(GameObject target, Transform fingertip){
        float distance = 0;
        distance = Vector3.Distance(target.transform.position, fingertip.position);
        return distance;
    }
}
