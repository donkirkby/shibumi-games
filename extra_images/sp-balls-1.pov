#include "colors.inc"  
#include "woods.inc"
#include "shapes.inc"
  
background{White}
  
camera 
{       
    orthographic
    look_at <0, 0, 0>     
    location <0, 0, 2.5>

    //look_at <0, 1.25, 0>     
    //location <0, 10.5, 0>
    //right <1, 0, 0>
}

//-----------------------------------------------------------------------------
// Light sources
  
/*  
light_source 
{  
   <-200, 400, 200> rgb <1.5, 1.5, 1.5> //rgb <2.2 2.25 2.25> 
   area_light <250, 0, 0>, <0, 0, 250>, 3, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <20, 20, 30> rgb <.25,.25,.25> //rgb <2.2 2.25 2.25>   
   area_light <0, 8, 0>, <0, 0, 8>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <40, 10, 5> rgb <.125,.125,.125> //rgb <2.2 2.25 2.25>   
   area_light <0, 8, 0>, <0, 0, 8>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <-50, 0, 100> rgb <.5, .5, .5> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <50, 0, -10> rgb <.5, .5, .5> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  
*/

union
{
light_source 
{  
   <-200, 400, 200> rgb <1,1,1> //rgb <2.2 2.25 2.25> 
   area_light <250, 0, 0>, <0, 0, 250>, 3, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{  
   <-200, 400, 200> rgb <.5,.5,.5> //rgb <2.2 2.25 2.25> 
   area_light <250, 0, 0>, <0, 0, 250>, 100, 100  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <20, 20, 30> rgb <.25,.25,.25> //rgb <2.2 2.25 2.25>   
   area_light <0, 8, 0>, <0, 0, 8>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <40, 10, 5> rgb <.125,.125,.125> //rgb <2.2 2.25 2.25>   
   area_light <0, 8, 0>, <0, 0, 8>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <50, -5, -30> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <50, -5, -40> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <50, -5, -50> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <50, -5, -60> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source 
{ 
   <50, -5, -80> rgb <.05,.05,.05> //rgb <2.2 2.25 2.25>   
   area_light <0, .1, 0>, <0, 0,.1>, 9, 3  // 5, 5
   adaptive 1
   jitter       
}                  

/*
// Backlight
light_source 
{ 
   <0, -50, -100> rgb <.5,.5,.5> //rgb <2.2 2.25 2.25>   
   area_light <250, 0, 0>, <0, 0, 250>, 3, 3  // 5, 5
   adaptive 1
   jitter       
}                  

light_source
{ <150, -200, -400>/50, <1, 1, 1>
  fade_distance 5 fade_power 2
  area_light x*3, y*3, 12, 12 circular orient adaptive 0
}
*/

   rotate <30, 0, -45>
}

//-----------------------------------------------------------------------------
            
#declare unit  = 1;
#declare dx    = unit / 2;
#declare dy    = unit * sqrt(3) / 2;
#declare r     = unit / 2.0;
#declare round = unit * 0.3;

#declare r_dot = 0.15 * unit;

// Small hex size
#declare x0 = -2*dx;
#declare y0 =     0;
#declare x1 =   -dx;
#declare y1 =    dy;
#declare x2 =    dx;
#declare y2 =    dy;
#declare x3 =  2*dx;
#declare y3 =     0;
#declare x4 =    dx;
#declare y4 =   -dy;
#declare x5 =   -dx;              

#declare y5 =   -dy;
                 
// Large hex size
#declare dxx = unit / 2 + round / 2;
#declare dyy = (unit + round) * sqrt(3) / 2;
                 
#declare xx0 = -2*dxx;
#declare yy0 =     0;
#declare xx1 =   -dxx;
#declare yy1 =    dyy;
#declare xx2 =    dxx;
#declare yy2 =    dyy;
#declare xx3 =  2*dxx;
#declare yy3 =     0;
#declare xx4 =    dxx;
#declare yy4 =   -dyy;
#declare xx5 =   -dxx;
#declare yy5 =   -dyy;               
                 
#declare SmallHexTile =
prism 
{
    linear_sweep linear_spline -round, round, 
    6, <x0, y0>, <x1, y1>, <x2, y2>, <x3, y3>, <x4,y4>, <x5, y5>
    rotate <90, 0, 0>
} 
                 
#declare LargeHexTile =
prism 
{
    linear_sweep linear_spline -1*round, 1 * round, 
    6, <xx0, yy0>, <xx1, yy1>, <xx2, yy2>, <xx3, yy3>, <xx4,yy4>, <xx5, yy5>
    rotate <90, 0, 0>
} 

#declare SmoothHexTile =
object
{
  difference
  {
    union
    {    
      sphere { <x0, y0, 0> round }
      sphere { <x1, y1, 0> round }
      sphere { <x2, y2, 0> round }
      sphere { <x3, y3, 0> round }
      sphere { <x4, y4, 0> round }
      sphere { <x5, y5, 0> round }
    
      cylinder { <x0, y0, 0> <x1, y1, 0> round }
      cylinder { <x1, y1, 0> <x2, y2, 0> round }
      cylinder { <x2, y2, 0> <x3, y3, 0> round }
      cylinder { <x3, y3, 0> <x4, y4, 0> round }
      cylinder { <x4, y4, 0> <x5, y5, 0> round }
      cylinder { <x5, y5, 0> <x0, y0, 0> round }
    
      object { SmallHexTile }
    }
    sphere { <0, 0, round> r_dot }
  }
}

//-----------------------------------------------------------------------------

#declare Tile =
   object
   {
       difference 
       {
   	   object { LargeHexTile }
   	   cylinder { <0, 0, -10> <0, 0, 10> .625  }
       } 
    	texture 
    	{ 
    	   pigment {color <0, 0.5, 1.0> }   
          normal { bumps 0.2 scale 0.025 }
          finish { ambient 0.25 diffuse 0.25 specular .25 roughness .1 } //reflection .025 }
    	} 
       //no_shadow 
   }

//-----------------------------------------------------------------------------

#declare rb = .3;
#declare rc = .75;
#declare th = 1;

#declare Board =
   object
   {
   	difference
   	{
   	   	union
   	       {
   		      box {<-1.5, -2.25,-th> <1.5,  2.25, 0>}
   	             box {<-2.25,-1.5, -th> <2.25, 1.5,  0>}
   	             cylinder { <-1.5,-1.5, -th> <-1.5,-1.5, 0> rc }
   	             cylinder { <-1.5, 1.5, -th> <-1.5, 1.5, 0> rc }
   	             cylinder { < 1.5,-1.5, -th> < 1.5,-1.5, 0> rc  }
   	             cylinder { < 1.5, 1.5, -th> < 1.5, 1.5, 0> rc  }
   		 }
   		 cylinder { <-1.5,-1.5, -2> <-1.5,-1.5, 1> rb  }
   		 cylinder { <-0.5,-1.5, -2> <-0.5,-1.5, 1> rb  }
   		 cylinder { < 0.5,-1.5, -2> < 0.5,-1.5, 1> rb  }
   		 cylinder { < 1.5,-1.5, -2> < 1.5,-1.5, 1> rb  }

   		 cylinder { <-1.5,-0.5, -2> <-1.5,-0.5, 1> rb  }
   		 cylinder { <-0.5,-0.5, -2> <-0.5,-0.5, 1> rb  }
   		 cylinder { < 0.5,-0.5, -2> < 0.5,-0.5, 1> rb  }
   		 cylinder { < 1.5,-0.5, -2> < 1.5,-0.5, 1> rb  }

   		 cylinder { <-1.5, 0.5, -2> <-1.5, 0.5, 1> rb  }
   		 cylinder { <-0.5, 0.5, -2> <-0.5, 0.5, 1> rb  }
   		 cylinder { < 0.5, 0.5, -2> < 0.5, 0.5, 1> rb  }
   		 cylinder { < 1.5, 0.5, -2> < 1.5, 0.5, 1> rb  }

   		 cylinder { <-1.5, 1.5, -2> <-1.5, 1.5, 1> rb  }
   		 cylinder { <-0.5, 1.5, -2> <-0.5, 1.5, 1> rb  }
   		 cylinder { < 0.5, 1.5, -2> < 0.5, 1.5, 1> rb  }
   		 cylinder { < 1.5, 1.5, -2> < 1.5, 1.5, 1> rb  }
   	}
       //difference 
       //{
   	//   object { LargeHexTile }
   	//   cylinder { <0, 0, -10> <0, 0, 10> .625  }
      // } 
    	texture 
    	{ 
    	   pigment {color <0, 0.5, 1.0> }   
          normal { bumps 0.2 scale 0.025 }
          finish { ambient 0.25 diffuse 0.25 specular .25 roughness .1 } //reflection .025 }
    	} 
       //no_shadow 
   }

//-----------------------------------------------------------------------------

#declare BallW =
	sphere 
	{
   		<0, 0, 0>, 1
   		pigment {color <.975, .96, .8> }   
   		finish { ambient 0.5 diffuse 0.35 specular .9 roughness .005 reflection .025 }  
   		//no_shadow
	}

#declare BallB =
	sphere 
	{
   		<0, 0, 0>, 1
   		//pigment {color <.05, 0, .0> }   
   		pigment {color <.15, .1333, .1333> }   
   		//finish { ambient 0.2 diffuse 0.3 phong 0.3 phong_size 10 specular .4 roughness .05 reflection .025 } //specular .9 roughness .005 reflection .05 }  
   		//finish { ambient 0.5 diffuse 0.3 phong 0.15 phong_size 5 specular .3 roughness .075 reflection .025 }  
   		finish { ambient 0.5 diffuse 0.35 specular .9 roughness .005 reflection .025 }  
   		//no_shadow
	}
	
#declare BallR =
	sphere 
	{
   		<0, 0, 0>, 1
   		pigment {color <.85, 0, 0> }   
   		finish { ambient 0.5 diffuse 0.35 phong 0.1 phong_size 2 specular .8 roughness .005 reflection .05 }  
   		//no_shadow
	}
	
//-----------------------------------------------------------------------------

union
{
   //object { Board }
   //object { BallW translate <0, 0, .95> }
   object { BallB translate <0, 0, .95> }
   //object { BallB translate <0, 1, 1.95> }
   //object { BallR translate <0, 0, .95> }

   #if (0)
   object { Tile0 translate < 2.5*(dx+round),  0, 0> }
   object { Tile1 translate <   0*(dx+round),  1*(dy+round), 0> }
   object { Tile2 translate <   0*(dx+round), -1*(dy+round), 0> }
   object { Tile3 translate <-2.5*(dx+round),  0, 0> }
   #end
  
   #if (0)    
   object
   {
      box 
      { 
         <-10, -10, -10> <10, 10, -1*round>       
         texture 
         { 
            pigment { color rgb <.45, .45, .45> } //White } 
            finish { reflection .8 }
         }
      }
   }  
   #end
   
   //no_shadow
  
   rotate <-5, 0, 0>
   //rotate <-60, 0, 0>
}
