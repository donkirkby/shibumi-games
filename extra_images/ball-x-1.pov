#include "scene.inc"


union
{
   object {
	sphere
	{
   		<0, 0, 0>, 1.0
   		texture { pigment {color <.3, .3, .3> } }
   		texture { pigment {
   		 image_map { png "x-8x.png" once interpolate 2 }
   		 translate <-0.5 , -0.5, 1>
   		 scale <1.25, 1.25, 1>
   		} }
   		finish { ambient 0.5 diffuse 0.35 specular .9 roughness .005 reflection .025 }
   		rotate <5, -10, 0>
	}
    translate <0, 0, .95> }

   rotate <-5, 0, 0>
}
