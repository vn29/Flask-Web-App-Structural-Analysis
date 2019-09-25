

class CScene():
    """Builds the list of lists that will be passed to the jinja2 template engine. meant to be placed into the javascript"""
    def __init__(self):
      #generate body to be fed into three.js rendering engine
      self.body()
      self.body_string = '\n'.join(str(r) for v in self.bodyvar for r in v) 

    def body(self):
      #construction of the body which is the script which governs what is generated
      self.bodyvar = [
            self.fscene_setup()
            + self.forbit()
            + self.fset_camera_pos()            
            #+ self.fcube()
            + self.fline(line_var_name="line1",i=(0,0,0),j=(0,10,0))
            + self.fline(line_var_name="line2",i=(0,10,0),j=(10,10,0))
            + self.fline(line_var_name="line3",i=(10,0,0),j=(10,10,0))
            + self.fsphere()
            + self.fraycaster()
            + self.f_onDocumentMouseMove()
            + self.fanimation_open()
            #+ self.fcubeanimate(cube_var_name = "cube",xrot = 0.0, yrot = 0.0)
            + self.f_find_intersects()
            + self.fanimation_close()
            ]

    def fscene_setup(self):
      return ['''var scene = new THREE.Scene();
            var camera = new THREE.PerspectiveCamera( 70, window.innerWidth / window.innerHeight, 1, 1000 );
            var renderer = new THREE.WebGLRenderer( { antialias: true } );
            var raycaster, parentTransform, sphereInter;
            var currentIntersected;
            var mouse = new THREE.Vector2();
            var radius = 100, theta = 0;
            renderer.setPixelRatio( window.devicePixelRatio );
            renderer.setSize( window.innerWidth/2, window.innerHeight/2 );
            container.appendChild( renderer.domElement );
            ''']

    def forbit(self):
      return ['''var controls = new THREE.OrbitControls( camera, renderer.domElement );
            window.addEventListener( 'resize', onWindowResize, false );
            function onWindowResize() {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize( window.innerWidth/2, window.innerHeight/2 );
            }''']

    def fline(self,line_var_name="line",i=(0,0,0), j=(1,1,1),  color="{ color: 0x00ff00 }"):
      return ['''var material = new THREE.LineBasicMaterial({7});
      var geometry = new THREE.Geometry();
      geometry.vertices.push(
            new THREE.Vector3( {1}, {2}, {3} ),
            new THREE.Vector3( {4}, {5}, {6} ),
      );
      var {0} = new THREE.Line( geometry, material );
      scene.add( {0} );'''.format(line_var_name, i[0], i[1], i[2], j[0], j[1], j[2], color)]


    def fsphere(self):
      return ['''
            var geometry = new THREE.SphereBufferGeometry( .1 );
            var material = new THREE.MeshBasicMaterial( { color: 0xff0000 } );
            sphereInter = new THREE.Mesh( geometry, material );
            sphereInter.visible = false;
            scene.add( sphereInter );
            ''']

    def fcube(self,cube_var_name="cube",x_dim=1,y_dim=1,z_dim=1,color="{ color: 0x00ff00 }"):
      return ['''var geometry = new THREE.BoxGeometry( {1}, {2}, {3} );
            var material = new THREE.MeshBasicMaterial( {4} );
            var {0} = new THREE.Mesh( geometry, material );
            scene.add( {0} );'''.format(cube_var_name, x_dim, y_dim, z_dim, color)]  

    def fset_camera_pos(self,zpos=5):
      return ["camera.position.z = {0}".format(zpos)]

    def fraycaster(self):
      return ['''
            raycaster = new THREE.Raycaster();
            raycaster.linePrecision = .1;
            document.addEventListener( 'mousemove', onDocumentMouseMove, false );
            ''']    

    def f_onDocumentMouseMove(self):
      return ['''
            function onDocumentMouseMove( event ) {
                  event.preventDefault();
                  mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
                  mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;
            }
            ''']  

    def fanimation_open(self):
      return ['''
            var animate = function () {
            requestAnimationFrame( animate );''']

    def fcubeanimate(self,cube_var_name = "cube",xrot=0.01,yrot=0.01):
      return ['''{0}.rotation.x += {1};
            {0}.rotation.y += {2};'''.format(cube_var_name,xrot,yrot)]

    def f_find_intersects(self, object_instersect = "line2"):
      return ['''raycaster.setFromCamera( mouse, camera );
            var intersects = raycaster.intersectObjects( [line1, line2, line3], true);
            if ( intersects.length > 0 ) {
                  if ( currentIntersected !== undefined ) {
                        currentIntersected.material.linewidth = 1;
                  }
                  currentIntersected = intersects[ 0 ].object;
                  currentIntersected.material.linewidth = 5;
                  sphereInter.visible = true;
                  sphereInter.position.copy( intersects[ 0 ].point );
            } else {
                  if ( currentIntersected !== undefined ) {
                        currentIntersected.material.linewidth = 1;
                  }
                  currentIntersected = undefined;
                  sphereInter.visible = false;}''']

    def fanimation_close(self):
      return ['''
            renderer.render( scene, camera );
            };
            animate();''']

