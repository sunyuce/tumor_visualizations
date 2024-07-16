var dom = document.getElementById('container_graph');
var myChart = echarts.init(dom, 'dark', {
  renderer: 'canvas',
  useDirtyRect: false
});
var app = {};

var bce_loss = {
  Unet: [7.1256, 3.8476, 2.5821, 2.1611, 1.8698, 1.6876, 1.3043, 1.5423, 1.2356, 1.1267, 1.2261, 0.9255, 0.8649, 0.9143, 0.7938, 0.7833, 0.7628, 0.7724, 0.742, 0.7216],
  Fpn: [2.9426, 1.8176, 1.502, 1.5199, 1.6459, 1.6972, 1.0766, 1.1802, 1.2871, 1.2798, 0.7998, 0.7813, 0.7473, 0.7625, 0.7387, 0.724, 0.7481, 0.7356, 0.7438, 0.7244],
  Segnet: [6.1742, 3.1164, 2.1737, 1.8271, 1.6632, 1.4002, 1.4008, 1.2523, 1.2071, 1.0836, 0.8974, 0.8221, 0.7929, 0.8196, 0.757, 0.7576, 0.7833, 0.7461, 0.7411, 0.6985]
};

var average_iou = {
  Unet: [0.4778, 0.5761, 0.6222, 0.651, 0.6379, 0.6892, 0.7078, 0.6936, 0.7195, 0.7339, 0.7263, 0.7623, 0.7885, 0.7513, 0.7957, 0.7745, 0.7796, 0.7861, 0.7934, 0.8085],
  Fpn: [0.6548, 0.7437, 0.7544, 0.7591, 0.7369, 0.7281, 0.8045, 0.8115, 0.7795, 0.7625, 0.8476, 0.8466, 0.8476, 0.846, 0.8527, 0.8558, 0.8518, 0.8448, 0.8488, 0.8555],
  Segnet: [0.6182, 0.7304, 0.7526, 0.7523, 0.7271, 0.7752, 0.7508, 0.783, 0.774, 0.7901, 0.8107, 0.8248, 0.8277, 0.8388, 0.8524, 0.8538, 0.8297, 0.8527, 0.8424, 0.8616, 0.8491]
};

var average_dice = {
  Unet: [0.5064, 0.6039, 0.658, 0.6881, 0.6776, 0.7078, 0.7327, 0.7312, 0.7457, 0.7694, 0.7567, 0.7834, 0.8075, 0.7779, 0.8289, 0.8026, 0.8116, 0.8081, 0.8226, 0.8358],
  Fpn: [0.6896, 0.7699, 0.7893, 0.7892, 0.7739, 0.7636, 0.8365, 0.843, 0.8168, 0.7978, 0.8797, 0.8776, 0.8791, 0.8769, 0.8852, 0.8869, 0.8829, 0.8767, 0.8811, 0.8871],
  Segnet: [0.6386, 0.755, 0.7804, 0.7831, 0.7574, 0.8011, 0.7827, 0.8133, 0.8004, 0.8219, 0.8406, 0.8538, 0.8576, 0.8677, 0.8815, 0.8827, 0.8598, 0.8808, 0.8709, 0.8897, 0.8817]
};

function updateChart(dataType) {
  var data;
  if (dataType === 'Val_loss') {
    data = bce_loss;
  } else if (dataType === 'mIoU') {
    data = average_iou;
  } else if (dataType === 'Dice') {
    data = average_dice;
  }

  option.series[0].data = data.Unet;
  option.series[1].data = data.Fpn;
  option.series[2].data = data.Segnet;

  myChart.setOption(option);
}

var option = {
  title: {
    // text: 'Stacked Line'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Unet', 'Fpn', 'Segnet']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  toolbox: {
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'],
    axisLabel: {
      rotate: 45
    }
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Unet',
      type: 'line',
      smooth: true,
      data: bce_loss.Unet
    },
    {
      name: 'Fpn',
      type: 'line',
      smooth: true,
      data: bce_loss.Fpn
    },
    {
      name: 'Segnet',
      type: 'line',
      smooth: true,
      data: bce_loss.Segnet
    }
  ]
};

if (option && typeof option === 'object') {
  myChart.setOption(option);
}

document.getElementById('dataSelect').addEventListener('change', function() {
  updateChart(this.value);
});

window.addEventListener('resize', myChart.resize);
