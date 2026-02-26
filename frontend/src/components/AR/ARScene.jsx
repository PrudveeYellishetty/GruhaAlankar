/**
 * ARScene Component - Handles Three.js + WebXR AR rendering
 * Production-ready, optimized, and isolated AR module
 */
import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import './ARScene.css';

const ARScene = ({ modelUrl, color, furnitureName, arSupported }) => {
  const containerRef = useRef(null);
  const sceneRef = useRef(null);
  const rendererRef = useRef(null);
  const cameraRef = useRef(null);
  const furnitureRef = useRef(null);
  const reticleRef = useRef(null);
  const hitTestSourceRef = useRef(null);
  const hitTestSourceRequestedRef = useRef(false);
  const sessionRef = useRef(null);
  
  const [isARActive, setIsARActive] = useState(false);
  const [modelLoaded, setModelLoaded] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!containerRef.current) return;

    initScene();
    
    return () => {
      cleanup();
    };
  }, []);

  useEffect(() => {
    if (modelUrl) {
      loadModel(modelUrl);
    }
  }, [modelUrl]);

  useEffect(() => {
    if (furnitureRef.current && color) {
      updateModelColor(color);
    }
  }, [color]);

  const initScene = () => {
    // Scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // Camera
    const camera = new THREE.PerspectiveCamera(
      70,
      window.innerWidth / window.innerHeight,
      0.01,
      20
    );
    cameraRef.current = camera;

    // Renderer
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true
    });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.xr.enabled = true;
    renderer.outputEncoding = THREE.sRGBEncoding;
    rendererRef.current = renderer;

    containerRef.current.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 5, 5);
    scene.add(directionalLight);

    // Reticle (placement indicator)
    const reticleGeometry = new THREE.RingGeometry(0.15, 0.2, 32);
    const reticleMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      side: THREE.DoubleSide
    });
    const reticle = new THREE.Mesh(reticleGeometry, reticleMaterial);
    reticle.matrixAutoUpdate = false;
    reticle.visible = false;
    scene.add(reticle);
    reticleRef.current = reticle;

    // Handle window resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    // Animation loop
    renderer.setAnimationLoop(render);
  };

  const loadModel = async (url) => {
    try {
      setModelLoaded(false);
      
      const loader = new GLTFLoader();
      const gltf = await new Promise((resolve, reject) => {
        loader.load(
          url,
          resolve,
          undefined,
          reject
        );
      });

      const model = gltf.scene;
      
      // Center and scale model
      const box = new THREE.Box3().setFromObject(model);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      
      model.position.sub(center);
      
      // Scale to reasonable size (max 1.5m)
      const maxDim = Math.max(size.x, size.y, size.z);
      if (maxDim > 1.5) {
        const scale = 1.5 / maxDim;
        model.scale.multiplyScalar(scale);
      }

      model.visible = false; // Hidden until placed
      
      if (furnitureRef.current) {
        sceneRef.current.remove(furnitureRef.current);
      }
      
      furnitureRef.current = model;
      sceneRef.current.add(model);
      
      updateModelColor(color);
      setModelLoaded(true);
      
    } catch (err) {
      console.error('Error loading model:', err);
      setError('Failed to load 3D model');
    }
  };

  const updateModelColor = (newColor) => {
    if (!furnitureRef.current) return;

    furnitureRef.current.traverse((child) => {
      if (child.isMesh) {
        // Clone material to avoid affecting other meshes
        child.material = child.material.clone();
        child.material.color.set(newColor);
        child.material.needsUpdate = true;
      }
    });
  };

  const startAR = async () => {
    if (!arSupported || !modelLoaded) {
      setError('AR not ready');
      return;
    }

    try {
      const session = await navigator.xr.requestSession('immersive-ar', {
        requiredFeatures: ['hit-test'],
        optionalFeatures: ['dom-overlay'],
        domOverlay: { root: document.body }
      });

      sessionRef.current = session;
      await rendererRef.current.xr.setSession(session);
      
      session.addEventListener('end', onSessionEnd);
      setIsARActive(true);

    } catch (err) {
      console.error('Error starting AR:', err);
      setError('Failed to start AR session');
    }
  };

  const onSessionEnd = () => {
    hitTestSourceRef.current = null;
    hitTestSourceRequestedRef.current = false;
    sessionRef.current = null;
    setIsARActive(false);
    
    if (furnitureRef.current) {
      furnitureRef.current.visible = false;
    }
    if (reticleRef.current) {
      reticleRef.current.visible = false;
    }
  };

  const render = (timestamp, frame) => {
    if (!frame || !sceneRef.current || !cameraRef.current || !rendererRef.current) {
      return;
    }

    const session = rendererRef.current.xr.getSession();
    if (session) {
      // Request hit test source
      if (!hitTestSourceRequestedRef.current) {
        session.requestReferenceSpace('viewer').then((referenceSpace) => {
          session.requestHitTestSource({ space: referenceSpace }).then((source) => {
            hitTestSourceRef.current = source;
          });
        });
        hitTestSourceRequestedRef.current = true;

        // Handle placement
        session.addEventListener('select', onSelect);
      }

      // Perform hit testing
      if (hitTestSourceRef.current && frame) {
        const referenceSpace = rendererRef.current.xr.getReferenceSpace();
        const hitTestResults = frame.getHitTestResults(hitTestSourceRef.current);

        if (hitTestResults.length > 0 && reticleRef.current) {
          const hit = hitTestResults[0];
          const pose = hit.getPose(referenceSpace);

          reticleRef.current.visible = true;
          reticleRef.current.matrix.fromArray(pose.transform.matrix);
        } else if (reticleRef.current) {
          reticleRef.current.visible = false;
        }
      }
    }

    rendererRef.current.render(sceneRef.current, cameraRef.current);
  };

  const onSelect = () => {
    if (reticleRef.current && reticleRef.current.visible && furnitureRef.current) {
      // Place furniture at reticle position
      const position = new THREE.Vector3();
      const quaternion = new THREE.Quaternion();
      const scale = new THREE.Vector3();
      
      reticleRef.current.matrix.decompose(position, quaternion, scale);
      
      furnitureRef.current.position.copy(position);
      furnitureRef.current.quaternion.copy(quaternion);
      furnitureRef.current.visible = true;
      
      // Hide reticle after placement
      reticleRef.current.visible = false;
    }
  };

  const cleanup = () => {
    if (sessionRef.current) {
      sessionRef.current.end();
    }

    if (rendererRef.current) {
      rendererRef.current.dispose();
    }

    if (sceneRef.current) {
      sceneRef.current.traverse((object) => {
        if (object.geometry) object.geometry.dispose();
        if (object.material) {
          if (Array.isArray(object.material)) {
            object.material.forEach(mat => mat.dispose());
          } else {
            object.material.dispose();
          }
        }
      });
    }
  };

  return (
    <div className="ar-scene-container" ref={containerRef}>
      {!isARActive && (
        <div className="ar-overlay">
          <div className="ar-preview">
            <h2>{furnitureName}</h2>
            {error && <p className="error-text">{error}</p>}
            {!modelLoaded && <p>Loading 3D model...</p>}
            {modelLoaded && arSupported && (
              <button
                onClick={startAR}
                className="start-ar-btn"
              >
                Start AR Experience
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ARScene;
