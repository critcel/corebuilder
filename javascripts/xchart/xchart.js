(function () {
var data = {
  "xScale": "ordinal",
  "yScale": "linear",
  "main": [
    {
      "className": ".scaleup",
      "data": [
  
        { "x": "1x1", "y": 4 },    
  
        { "x": "2x2", "y": 8 },    
  
        { "x": "3x3", "y": 8 },    
  
      ]
    }
  ]
};
var myChart = new xChart('bar', data, '#example1');
}());
