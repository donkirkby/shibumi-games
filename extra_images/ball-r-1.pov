#include "scene.inc"


union
{
   object {
	sphere
	{
   		<0, 0, 0>, 1
   		pigment {color <.85, 0, 0> }
   		finish { ambient 0.5 diffuse 0.35 phong 0.1 phong_size 2 specular .8 roughness .005 reflection .05 }
	}
    translate <0, 0, .95> }

   rotate <-5, 0, 0>
}
