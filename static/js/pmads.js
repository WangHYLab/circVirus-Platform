function handlePeptideSequenceClick(element) {
  // 获取元素内容
  var sequence = element.textContent;
  // 去除括号中的内容
  var cleanedSequence = sequence.replace(/\(.*?\)/g, "");
  // 构建跳转的 URL
  var url =
    "https://www.proteomicsdb.org/search?q=" +
    cleanedSequence +
    "&type=Peptide&projectId=-1";
  // 跳转到新 URL
  window.location.href = url;
};

// 获取剂量曲线
function handleDecryptMCurveClick1(element) {
  // 获取元素的 getid 属性值
  var id = element.getAttribute('getid');
  //   console.log(id);
  // 发送 AJAX 请求
  $.ajax({
    url: '/pmads/api/getdosecurve',
    type: 'GET',
    data: { 'id': id },
    success: function (response) {
      // 处理响应
      console.log(response);
      // 响应处理
      // 创建模态框HTML
      // 创建弹窗元素
      var overlay = document.createElement('div');
      overlay.style.position = 'fixed';
      overlay.style.top = '0';
      overlay.style.left = '0';
      overlay.style.width = '100%';
      overlay.style.height = '100%';
      overlay.style.backgroundColor = 'rgba(0,0,0,0.7)';
      overlay.style.zIndex = '1000';
      overlay.style.display = 'flex';
      overlay.style.justifyContent = 'center';
      overlay.style.alignItems = 'center';

      var popup = document.createElement('div');
      popup.style.backgroundColor = '#fff';
      popup.style.padding = '20px';
      popup.style.borderRadius = '5px';
      popup.style.position = 'relative';
      popup.style.maxWidth = '90%';
      popup.style.maxHeight = '90%';
      popup.style.overflow = 'auto';

      var closeBtn = document.createElement('button');
      closeBtn.innerHTML = '×';
      closeBtn.style.position = 'absolute';
      closeBtn.style.top = '5px';
      closeBtn.style.right = '5px';
      closeBtn.style.background = 'none';
      closeBtn.style.border = 'none';
      closeBtn.style.fontSize = '20px';
      closeBtn.style.cursor = 'pointer';

      var img = document.createElement('img');
      img.src = response.url;
      img.style.width = '300px';
      img.style.height = '250px';
      img.style.display = 'block';

      popup.appendChild(closeBtn);
      popup.appendChild(img);
      overlay.appendChild(popup);
      document.body.appendChild(overlay);

      closeBtn.onclick = function () {
        document.body.removeChild(overlay);
      };

      overlay.onclick = function (e) {
        if (e.target === overlay) {
          document.body.removeChild(overlay);
        }
      };
    },
    error: function (error) {
      // 处理错误
      console.log(error);
    }
  });
};

function handleDecryptMCurveClick(element) {
  var id = element.getAttribute("getid");

  $.ajax({
    url: "/pmads/api/getdosecurve",
    type: "GET",
    data: { id: id },
    success: function (response) {
      // 确保 response 是对象且包含 url
      var data = typeof response === "string" ? JSON.parse(response) : response;
      var imageUrl = data.url || data.imageUrl; // 根据实际字段调整

      console.log("Image URL to load:", imageUrl);

      // 创建模态框
      // var modalHTML = `
      //           <div class="modal fade" id="imageModal" tabindex="-1">
      //               <div class="modal-dialog modal-lg">
      //                   <div class="modal-content">
      //                       <div class="modal-header">
      //                           <h5 class="modal-title">剂量曲线图</h5>
      //                           <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      //                       </div>
      //                       <div class="modal-body text-center">

      //                           <img src="${imageUrl}" class="img-fluid" onerror="this.onerror=null;">
      //                       </div>
      //                   </div>
      //               </div>
      //           </div>
      //       `;

      // // 移除旧的模态框（如果存在）
      // $("#imageModal").remove();
      // $("body").append(modalHTML);

      // // 显示模态框（Bootstrap 5+ 用法）
      // var modal = new bootstrap.Modal(document.getElementById("imageModal"));
      // modal.show();
      var overlay = document.createElement("div");
      overlay.style.position = "fixed";
      overlay.style.top = "0";
      overlay.style.left = "0";
      overlay.style.width = "100%";
      overlay.style.height = "100%";
      overlay.style.backgroundColor = "rgba(0,0,0,0.7)";
      overlay.style.zIndex = "1000";
      overlay.style.display = "flex";
      overlay.style.justifyContent = "center";
      overlay.style.alignItems = "center";

      // 创建弹窗内容
      var popup = document.createElement("div");
      popup.style.backgroundColor = "#fff";
      popup.style.padding = "20px";
      popup.style.borderRadius = "5px";
      popup.style.position = "relative";

      // 创建关闭按钮
      var closeBtn = document.createElement("button");
      closeBtn.innerHTML = "×";
      closeBtn.style.position = "absolute";
      closeBtn.style.top = "5px";
      closeBtn.style.right = "5px";
      closeBtn.style.background = "none";
      closeBtn.style.border = "none";
      closeBtn.style.fontSize = "20px";
      closeBtn.style.cursor = "pointer";

      // 创建图片
      var img = document.createElement("img");
      img.src = response.url;
      img.style.maxWidth = "70vw";
      img.style.maxHeight = "70vh";

      // 组装元素
      popup.appendChild(closeBtn);
      popup.appendChild(img);
      overlay.appendChild(popup);
      document.body.appendChild(overlay);

      // 点击关闭按钮或遮罩关闭弹窗
      closeBtn.onclick = function () {
        document.body.removeChild(overlay);
      };
      overlay.onclick = function (e) {
        if (e.target === overlay) {
          document.body.removeChild(overlay);
        }
      };
    },
    error: function (xhr, status, error) {
      console.error("AJAX Error:", status, error);
      alert("加载失败: " + (xhr.responseJSON?.message || "请稍后重试"));
    },
  });
}


function createLoadChartData(
  myChart,
  app,
  option,
  chartLoaded,
  proId,
  sitePos
) {
  return function () {
    console.log("监测中");
    if (chartLoaded) {
      return; // 如果已加载，则不再重复加载
    }
    $("#ptm-funcscore #funcscore-plot").show();
    const container = document.getElementById("funcscore-plot");
    const rect = container.getBoundingClientRect();
    // 判断容器是否在视口内（可以根据您的需求调整触发加载的条件）
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      const proteinId = proId; // 您要传递的蛋白质ID
      const apiUrl = "/pmads/api/getfuncscore?id=" + proteinId;

      fetch(apiUrl)
        .then((response) => response.json())
        .then((data) => {
          const annoData = JSON.parse(data);
          const chartData = annoData.map(function (item) {
            return [parseInt(item.Position), parseFloat(item.Score)];
          });

          const highlightXValue = sitePos; // 示例高亮值

          option = {
            xAxis: {
              type: "value",
              name: "Position",
              nameLocation: "center",
              nameGap: 25,
              nameTextStyle: {
                padding: [5, 0, 0, 0],
                color: "black",
                fontSize: 12,
                fontWeight: "bold",
              },
              axisLabel: {
                formatter: function (value) {
                  return Math.round(value); // 使用 Math.floor() 取整
                  // 或者使用 Math.round(value); // 使用 Math.round() 四舍五入取整
                },
                align: "center",
              },
              axisLine: {
                lineStyle: {
                  width: 2,
                },
              },
              splitLine: {
                show: false,
              },
            },
            yAxis: {
              type: "value",
              name: "Phos Site Score",
              nameLocation: "center",
              nameGap: 25,
              nameTextStyle: {
                padding: [0, 0, 5, 0],
                color: "black",
                fontSize: 12,
                fontWeight: "bold",
              },
              max: 1,
              min: 0,
              splitLine: {
                show: false,
              },
            },
            tooltip: {
              trigger: "axis",
              axisPointer: {
                type: "cross",
              },
              formatter: function (params) {
                let res =
                  "Position: " + Math.floor(params[0].value[0]) + "<br>";
                for (let i = 0; i < params.length; i++) {
                  if (params[i].seriesType === "scatter") {
                    res +=
                      params[i].marker +
                      " " +
                      params[i].seriesName +
                      ": " +
                      params[i].value[1] +
                      "<br>";
                  }
                }
                return res;
              },
            },
            // toolbox: {
            //   show: true,
            //   feature: {
            //     saveAsImage: {},
            //   },
            // },
            series: [
              {
                name: "Bar Value",
                type: "bar",
                barWidth: 3,
                borderWidth: 0,
                data: chartData.map((item) => ({
                  value: item,
                  itemStyle: {
                    color: item[0] === highlightXValue ? "#f5b1aa" : "#b1d5c8",
                    pattern: null,
                  },
                })),
                tooltip: {
                  show: false,
                },
              },
              {
                name: "Score",
                type: "scatter",
                symbol: "circle",
                symbolSize: 15,
                itemStyle: {
                  color: "#EE6666",
                  borderColor: "#EE6666",
                  borderWidth: 0,
                },
                data: chartData.map(function (item) {
                  const isHighlight = item[0] === highlightXValue;
                  return {
                    value: item,
                    symbolSize: isHighlight ? 20 : 15,
                    itemStyle: {
                      color: isHighlight ? "#FF0000" : "#fd7e14",
                    },
                    label: {
                      show: isHighlight, // 只有高亮的点显示label
                      position: "top", // 标签位置
                      formatter: function (params) {
                        return params.value[1]; // 标签显示内容
                      },
                      fontSize: 12,
                      color: "#FF0000",
                      fontWeight: "bold",
                    },
                  };
                }),
              },
            ],
          };

          if (option && typeof option === "object") {

            myChart.setOption(option);
            chartLoaded = true; // 标记为已加载
            window.removeEventListener("scroll", this); // 移除滚动监听
            window.removeEventListener("resize", this); // 移除resize监听
            $("#ptm-funcscore .no-data").hide();

          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
          $("#ptm-funcscore .no-data").show();
          $("#ptm-funcscore #funcscore-plot").hide();
        });
    }
  };
}

function debounce(func, delay) {
  let timeoutId;
  return function (...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
    }, delay);
  };
}

// 结构绘图
function loadProteinStructure(structureBox,
  structureHasLoaded,
  pdbId,
  sitePos) {
  return function () {
    console.log("参数：");
    console.log("structureBox:", structureBox);
    console.log("structureHasLoaded:", structureHasLoaded);
    console.log("pdbId:", pdbId);
    console.log("sitePos:", sitePos);
    
    if (structureHasLoaded) {
      return; // 如果已加载，则不再执行
    }
    structureHasLoaded = true;

    // 创建NGL舞台对象
    var uniportId = document.getElementById("uniport-id").innerHTML;
    // var pdbId = document.getElementById("pdb_id").innerHTML;
    var stage = new NGL.Stage("structure-box");

    if (pdbId != "") {
      var pdbUrl = "https://files.rcsb.org/download/" + pdbId + ".pdb";
      var pdb3dlink = "https://www.rcsb.org/3d-view/" + pdbId;
      // e.g. https://files.rcsb.org/download/4hhb.pdb
    } else {
      var pdbUrl =
        "https://alphafold.ebi.ac.uk/files/AF-" + uniportId + "-F1-model_v4.pdb";
    }

    stage
      .loadFile(pdbUrl)
      // .loadFile("https://files.rcsb.org/download/5bve.pdb")
      .then(function (o) {
        o.addRepresentation("cartoon", {
          color: "sstruc",
          aspectRatio: 4,
          scale: 0.5,
        });
        o.addRepresentation("ball+stick", {
          sele: String(sitePos),
          // color:"red",
          scale: 4,
          aspectRatio: 1.5,
        });
        o.addRepresentation("surface", {
          sele: String(sitePos),
          opacity: 0.4,
          useWorker: false,
        });

        stage.autoView();
      })

      .catch(function (error) {
        console.error("Failed to load or process the structure:", error);
        // 在页面上显示错误信息，例如：
        if (structureBox) {
          structureBox.innerHTML =
            "<p style='color: red;'>Failed to load the protein structure.</p>";
          console.log("Displayed error message on the page.");
        }
      });

    // 添加窗口大小调整事件处理 (只有在加载后才需要)
    // window.addEventListener(
    //   "resize",
    //   function (event) {
    //     if (typeof stage !== "undefined") {
    //       stage.handleResize();
    //     }
    //   },
    //   false
    // );
    const elem = document.getElementById("structure-link");
    elem.href = pdb3dlink;
  }
}

function drawProteinStructure(
  pdbId,
  uniportId,
  sitePos,
  boxId
) {
  // console.log("绘制蛋白质结构：", pdbId, uniportId, sitePos, boxId);
  const viewerInstance = new PDBeMolstarPlugin();

  // Set options (uncomment lines to explore various options)
  const options = {
    moleculeId: pdbId,
    hideControls: true,
    customData: {
      url:
        "https://alphafold.ebi.ac.uk/files/AF-" +
        uniportId +
        "-F1-model_v4.cif",
      format: "cif",
      binary: false,
    },
    selection: {
      data: [
        {
          //struct_asym_id: 'T',
          start_residue_number: parseInt(sitePos),
          end_residue_number: parseInt(sitePos),
          color: "red",
        },
      ],
      nonSelectedColor: "#ddccbb",
    },
    visualStyle: "cartoon", // cartoon | ball-and-stick | carbohydrate | ellipsoid | gaussian-surface | molecular-surface | point | putty | spacefill
    hideStructure: ["het", "water"],
    landscape: true,
    sequencePanel: true,
    loadingOverlay: true,
    expanded: false,
  };
  const viewerContainer = document.getElementById(boxId);
  viewerInstance.render(viewerContainer, options);
}