var cancers = ["ACC", "ALL", "BLCA", "BRCA", "CESC", "CLL", "COREAD", "DLBC", "ESCA", "GBM", "HNSC", "KIRC", "LAML", "LCML", "LGG", "LIHC", "LUAD", "LUSC", "MB", "MESO", "MM", "NB", "OV", "PAAD", "PRAD", "SCLC", "SKCM", "STAD", "THCA", "UCEC"];
var cols = ["#7F2020", "#47CC33", "#80C4FF", "#C36CD9", "#C5CC66", "#002999", "#F28100", "#315916", "#2860FF", "#E55039", "#EEFF00", "#303E8A", "#F2AA79", "#007AE6", "#CEB6F2", "#663355", "#903BFF", "#539B51", "#996600", "#53A6A0", "#FF4E53", "#33260D", "#35C2B3", "#F200A2", "#FFCC00", "#40FFD9", "#AA2B2B", "#807960", "#13324D", "#FF8091"];

function count(arr, item) {
  return arr.filter((e) => e === item).length;
};

function getPieData(rawdata) {
  var piedata = [];
  for (var i = 0; i < cancers.length; i++) {
    // console.log(cancers[i]);
    var c = count(rawdata, cancers[i]);
    piedata[i] = {
      'name': cancers[i],
      'value': c
    };
  };
  return piedata;
};

var path = ["EGFR signaling", "PI3K/MTOR signaling", "RTK signaling", "Protein stability and degradation", "Mitosis", "Other", "ERK MAPK signaling", "Other, kinases", "ABL signaling", "Cell cycle", "IGF1R signaling", "Chromatin histone acetylation", "Cytoskeleton", "DNA replication", "Hormone-related", "Genome integrity", "WNT signaling", "JNK and p38 signaling", "Chromatin other", "Metabolism", "Apoptosis regulation", "Chromatin histone methylation", "p53 pathway", "Unclassified"]
var cols = ["#7F2020", "#47CC33", "#80C4FF", "#C36CD9", "#C5CC66", "#002999", "#F28100", "#315916", "#2860FF", "#E55039", "#EEFF00", "#303E8A", "#F2AA79", "#007AE6", "#CEB6F2", "#663355", "#903BFF", "#539B51", "#996600", "#53A6A0", "#FF4E53", "#33260D", "#35C2B3", "#F200A2", "#FFCC00", "#40FFD9", "#AA2B2B", "#807960", "#13324D", "#FF8091"];

function getPieDataHome(rawdata) {
  var piedata = [];
  for (var i = 0; i < path.length; i++) {
    // console.log(cancers[i]);
    var c = count(rawdata, path[i]);
    piedata[i] = {
      'name': path[i],
      'value': c
    };
  };
  return piedata;
};