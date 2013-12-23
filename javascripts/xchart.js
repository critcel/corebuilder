['1x1', '2x2', '3x3', '4x4', '5x5', '6x6', '7x7'] [7.0, 25.0, 60.0, 101.0, 160.0, 227.0, 326.0]
(function () {
var data = {
  "xScale": "ordinal",
  "yScale": "linear",
  "main": [
    {
      "className": ".scaleup",
      "data": [
  
        { "x": "1x1", "y": 7.0 },    
  
        { "x": "2x2", "y": 25.0 },    
  
        { "x": "3x3", "y": 60.0 },    
  
        { "x": "4x4", "y": 101.0 },    
  
        { "x": "5x5", "y": 160.0 },    
  
        { "x": "6x6", "y": 227.0 },    
  
        { "x": "7x7", "y": 326.0 },    
  
      ]
    }
  ]
};
var myChart = new xChart('bar', data, '#example1');
}());
