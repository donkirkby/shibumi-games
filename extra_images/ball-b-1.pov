#include "scene.inc"


union
{
   object {
	sphere
	{
   		<0, 0, 0>, 1
   		pigment {color <.06, .03, .03> }
   		finish { ambient 0.5 diffuse 0.35 specular .9 roughness .005 reflection .025 }
	}
    translate <0, 0, .95> }

   rotate <-5, 0, 0>
}
