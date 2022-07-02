using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Slider_Value : MonoBehaviour
{
    //Add your slider from the Editor
    public Slider sliderRef;
    //Add your light from the Editor
    public Light lightRef;

    void OnEnable()
    {
        //Subscribe to the Slider Click event
        sliderRef.onValueChanged.AddListener(sliderCallBack);
    }

    //Will be called when Slider changes
    void sliderCallBack(float value)
    {
        Debug.Log("Light Intensity: " + value);
        lightRef.intensity = sliderRef.value;
    }

    void OnDisable()
    {
        //Un-Subscribe To Slider Event
        sliderRef.onValueChanged.RemoveAllListeners();
    }
    
}
