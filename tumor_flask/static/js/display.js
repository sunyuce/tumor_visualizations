// 查找之前定义的用于可视化的div
        var myContainer = document.querySelector('#tumor_3D');

        // 用于页面可视化的Renderer，官方文档介绍是使用fullScreenRenderer
        var fullScreenRenderer = vtk.Rendering.Misc.vtkFullScreenRenderWindow.newInstance({
            background: [0.0, 0.0, 0.0],
            container: myContainer,  // 绑定myContainer
        });

        // 获取渲染器和渲染窗口
        var renderer = fullScreenRenderer.getRenderer();
        var renderWindow = fullScreenRenderer.getRenderWindow();

        // 定义actor和mapper
        var actor = vtk.Rendering.Core.vtkActor.newInstance();
        var mapper = vtk.Rendering.Core.vtkMapper.newInstance();

        // 定义vtpReader，读取.vtp文件
        const vtpReader = vtk.IO.XML.vtkXMLPolyDataReader.newInstance();

        // 进行inputConnection连接
        mapper.setInputConnection(vtpReader.getOutputPort());
        actor.setMapper(mapper);

        // 调整模型的颜色
        mapper.setScalarVisibility(true);
        // actor.getProperty().setColor(1.0, 1.0, 1.0);

        // 获取模型的中心点
        function getCenterOfMass() {
            const bounds = actor.getBounds();
            const center = [
                (bounds[0] + bounds[1]) / 2,
                (bounds[2] + bounds[3]) / 2,
                (bounds[4] + bounds[5]) / 2,
            ];
            return center;
        }
        // 保存初始相机状态
        let initialCameraState;

        function saveInitialCameraState() {
            const camera = renderer.getActiveCamera();
            initialCameraState = {
                position: [...camera.getPosition()],
                focalPoint: [...camera.getFocalPoint()],
                viewUp: [...camera.getViewUp()],
                clippingRange: [...camera.getClippingRange()]
            };
        }

        function resetCameraToInitialState() {
            const camera = renderer.getActiveCamera();
            camera.setPosition(...initialCameraState.position);
            camera.setFocalPoint(...initialCameraState.focalPoint);
            camera.setViewUp(...initialCameraState.viewUp);
            camera.setClippingRange(...initialCameraState.clippingRange);
            renderWindow.render();
        }

        // 设置渲染函数
        function beginRender() {
            renderer.addActor(actor);
            renderer.resetCamera();
            saveInitialCameraState();  // 保存初始相机状态
            renderWindow.render();
        }

        // 获取患者的Patient值
        var patientNumber = "{{ patient.Patient }}";

        // 动态设置vtp文件的路径
        var vtpUrl = "../static/combine/" + patientNumber + ".vtp";
        // 寻找模型存放的位置并开始渲染
        vtpReader.setUrl(vtpUrl).then(beginRender);
        // 寻找模型存放的位置并开始渲染
        // vtpReader.setUrl("../static/combine/TCGA_CS_5397.vtp").then(beginRender);

        function animateRotation(axis, angle) {
            const center = getCenterOfMass();
            actor.setOrigin(...center);

            const increment = 5;
            let currentAngle = 0;
            const animation = () => {
                if (currentAngle < angle) {
                    currentAngle += increment;
                    actor.rotateWXYZ(increment, ...axis);
                    renderWindow.render();
                    requestAnimationFrame(animation);
                }
            };
            animation();
        }
         // 控制按钮
        document.getElementById('rotateLeft').addEventListener('click', function () {
            animateRotation([0, 0, -1], 90);
        });

        document.getElementById('rotateRight').addEventListener('click', function () {
            animateRotation([0, 0, 1], 90);
        });

        document.getElementById('rotateUp').addEventListener('click', function () {
            animateRotation([1, 0, 0], 90);
        });

        document.getElementById('rotateDown').addEventListener('click', function () {
            animateRotation([-1, 0, 0], 90);
        });
        // 重置按钮的点击事件
        document.getElementById('resetButton').addEventListener('click', resetCameraToInitialState);
        // 图片切换功能
        // const imageContainer = document.getElementById('imageContainer');
        const imageContainer1 = document.getElementById('imageContainer1');
        const imageContainer2 = document.getElementById('imageContainer2');
        const imageContainer3 = document.getElementById('imageContainer3');
        const numImages = "{{num_images}}";
        let currentIndex = 0;
        const imagesPerGroup = 3;

        // function createImageElements(container, pathPrefix) {
        //     for (let i = 1; i <= numImages; i++) {
        //         const img = document.createElement('img');
        //         img.id = 'image' + i;
        //         img.src = `${pathPrefix}/image_${i}.png`;
        //         img.style.display = i < imagesPerGroup ? 'block' : 'none';
        //         img.addEventListener('click', function () {
        //             document.getElementById('modalImage').src = img.src;
        //             document.getElementById('myModal').style.display = "block";
        //         });
        //         container.appendChild(img);
        //     }
        // }
        function createImageElements(container, pathPrefix) {
            for (let i = numImages; i >= 1; i--) {
                const img = document.createElement('img');
                img.id = 'image' + i;
                img.src = `${pathPrefix}/image_${i}.png`;
                img.style.display = i > numImages - imagesPerGroup ? 'block' : 'none';
                img.addEventListener('click', function () {
                    document.getElementById('modalImage').src = img.src;
                    document.getElementById('myModal').style.display = "block";
                });
                container.appendChild(img);
            }
        }
        function createImageElements2(container, pathPrefix) {
            for (let i = numImages; i >= 1; i--) {
                const img = document.createElement('img');
                img.id = 'image' + i;
                img.src = `${pathPrefix}/cheat_${i}.png`;
                img.style.display = i > numImages - imagesPerGroup ? 'block' : 'none';
                img.addEventListener('click', function () {
                    document.getElementById('modalImage').src = img.src;
                    document.getElementById('myModal').style.display = "block";
                });
                container.appendChild(img);
            }
        }
        createImageElements(imageContainer1, `../static/brain_origin/${patientNumber}`);
        createImageElements(imageContainer2, `../static/brain_highlight/${patientNumber}`);
        createImageElements2(imageContainer3, `../static/heat_combine/${patientNumber}`);

        function updateButtons() {
            document.getElementById('prevButton').disabled = currentIndex === 0;
            document.getElementById('nextButton').disabled = currentIndex + imagesPerGroup >= numImages;
        }

        function updateImageContainers() {
            const images1 = document.querySelectorAll('#imageContainer1 img');
            const images2 = document.querySelectorAll('#imageContainer2 img');
            const images3 = document.querySelectorAll('#imageContainer3 img');
            images1.forEach((img, index) => {
                img.style.display = (index >= currentIndex && index < currentIndex + imagesPerGroup) ? 'block' : 'none';
            });
            images2.forEach((img, index) => {
                img.style.display = (index >= currentIndex && index < currentIndex + imagesPerGroup) ? 'block' : 'none';
            });
            images3.forEach((img, index) => {
                img.style.display = (index >= currentIndex && index < currentIndex + imagesPerGroup) ? 'block' : 'none';
            });
            updateButtons();
        }

        document.getElementById('prevButton').addEventListener('click', function () {
            if (currentIndex > 0) {
                currentIndex--;
                updateImageContainers();
            }
        });

        document.getElementById('nextButton').addEventListener('click', function () {
            if (currentIndex + imagesPerGroup < numImages) {
                currentIndex++;
                updateImageContainers();
            }
        });

        updateImageContainers();

        // Get the modal
        var modal = document.getElementById("myModal");
        var span = document.getElementsByClassName("close")[0];
        span.onclick = function() {
            modal.style.display = "none";
        }
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }