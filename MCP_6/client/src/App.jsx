import { useEffect, useState, useRef } from "react";
import { Excalidraw, convertToExcalidrawElements } from "@excalidraw/excalidraw";

// Types matching Server
const ElementType = ["rectangle", "ellipse", "diamond", "arrow", "text"];

function App() {
  const [excalidrawAPI, setExcalidrawAPI] = useState(null);
  const [status, setStatus] = useState("Disconnected");
  const [pendingScene, setPendingScene] = useState(null);
  const wsRef = useRef(null);

  // Convert Server Element -> Excalidraw Element
  const mapToExcalidraw = (elements) => {
    console.log("Mapping elements:", elements);
    const excalidrawElements = [];

    const baseElement = {
      version: 1,
      versionNonce: Math.floor(Math.random() * 1000000),
      isDeleted: false,
      fillStyle: "solid",
      strokeWidth: 2,
      strokeStyle: "solid",
      roughness: 1,
      opacity: 100,
      angle: 0,
      seed: Math.floor(Math.random() * 1000000),
      groupIds: [],
      frameId: null,
      roundness: null,
      boundElements: [],
      updated: Date.now(),
      link: null,
      locked: false,
    };

    elements.forEach(e => {
      if (e.type === "rectangle") {
        // Create rectangle
        const rectId = e.id;
        const textId = e.id + "-text";
        
        excalidrawElements.push({
          ...baseElement,
          type: "rectangle",
          id: rectId,
          x: e.x,
          y: e.y,
          width: e.width || 150,
          height: e.height || 60,
          strokeColor: e.strokeColor || "#000000",
          backgroundColor: e.backgroundColor || "transparent",
          fillStyle: e.fillStyle || "hachure",
        });

        // Create text element for the label
        if (e.text) {
          excalidrawElements.push({
            type: "text",
            version: 1,
            versionNonce: Math.floor(Math.random() * 1000000),
            isDeleted: false,
            id: textId,
            strokeWidth: 1,
            strokeStyle: "solid",
            roughness: 1,
            opacity: 100,
            angle: 0,
            x: e.x + 10,
            y: e.y + (e.height || 60) / 2 - 10,
            width: (e.width || 150) - 20,
            height: 20,
            strokeColor: "#000000", 
            backgroundColor: "transparent",
            fontSize: 20,
            fontFamily: 1,
            text: e.text,
            textAlign: "center",
            verticalAlign: "middle",
            originalText: e.text,
            seed: Math.floor(Math.random() * 1000000),
            groupIds: [],
            boundElements: [],
            updated: Date.now(),
            link: null,
            locked: false,
          });
        }
      } else if (e.type === "ellipse") {
        // Create ellipse
        const ellipseId = e.id;
        const textId = e.id + "-text";
        
        excalidrawElements.push({
          ...baseElement,
          type: "ellipse",
          id: ellipseId,
          x: e.x,
          y: e.y,
          width: e.width || 150,
          height: e.height || 60,
          strokeColor: e.strokeColor || "#000000",
          backgroundColor: e.backgroundColor || "transparent",
          fillStyle: e.fillStyle || "hachure",
        });

        // Create text element for the label
        if (e.text) {
          excalidrawElements.push({
            type: "text",
            version: 1,
            versionNonce: Math.floor(Math.random() * 1000000),
            isDeleted: false,
            id: textId,
            strokeWidth: 2,
            strokeStyle: "solid",
            roughness: 1,
            opacity: 100,
            angle: 0,
            x: e.x + 10,
            y: e.y + (e.height || 60) / 2 - 10,
            width: (e.width || 150) - 20,
            height: 20,
            strokeColor: "#000000", 
            backgroundColor: "transparent",
            fontSize: 20,
            fontFamily: 1,
            text: e.text,
            textAlign: "center",
            verticalAlign: "middle",
            originalText: e.text,
            seed: Math.floor(Math.random() * 1000000),
            groupIds: [],
            boundElements: [],
            updated: Date.now(),
            link: null,
            locked: false,
          });
        }
      } else if (e.type === "diamond") {
        // Create diamond
        const diamondId = e.id;
        const textId = e.id + "-text";
        
        excalidrawElements.push({
          ...baseElement,
          type: "diamond",
          id: diamondId,
          x: e.x,
          y: e.y,
          width: e.width || 150,
          height: e.height || 60,
          strokeColor: e.strokeColor || "#000000",
          backgroundColor: e.backgroundColor || "transparent",
          fillStyle: e.fillStyle || "hachure",
        });

        // Create text element for the label
        if (e.text) {
          excalidrawElements.push({
            type: "text",
            version: 1,
            versionNonce: Math.floor(Math.random() * 1000000),
            isDeleted: false,
            id: textId,
            strokeWidth: 2,
            strokeStyle: "solid",
            roughness: 1,
            opacity: 100,
            angle: 0,
            x: e.x + 10,
            y: e.y + (e.height || 60) / 2 - 10,
            width: (e.width || 150) - 20,
            height: 20,
            strokeColor: "#000000", 
            backgroundColor: "transparent",
            fontSize: 20,
            fontFamily: 1,
            text: e.text,
            textAlign: "center",
            verticalAlign: "middle",
            originalText: e.text,
            seed: Math.floor(Math.random() * 1000000),
            groupIds: [],
            boundElements: [],
            updated: Date.now(),
            link: null,
            locked: false,
          });
        }
      } else if (e.type === "arrow") {
         
        excalidrawElements.push({
          ...baseElement,
          type: "arrow",
          id: e.id,
          x: e.x || 0,
          y: e.y || 0,
          width: 100,
          height: 0,
          points: [[0, 0], [100, 0]],
          strokeColor: "#000000",
          backgroundColor: "transparent",
          startBinding: e.fromId ? { elementId: e.fromId, focus: 0.5, gap: 4 } : null,
          endBinding: e.toId ? { elementId: e.toId, focus: 0.5, gap: 4 } : null,
        });
      }
    });

    console.log("Mapped to Excalidraw elements:", excalidrawElements);
    return excalidrawElements;
  };

  const connectWs = () => {
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    const baseReconnectInterval = 1000; // 1 second

    const attemptConnect = () => {
      if (wsRef.current) wsRef.current.close();

      const ws = new WebSocket(`ws://127.0.0.1:${import.meta.env.VITE_WS_PORT}`);
      wsRef.current = ws;

      ws.onopen = () => {
        setStatus("Connected");
        reconnectAttempts = 0; // Reset on successful connection
      };

      ws.onclose = () => {
        setStatus("Disconnected");
        if (reconnectAttempts < maxReconnectAttempts) {
          const delay = baseReconnectInterval * Math.pow(2, reconnectAttempts);
          console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts + 1}/${maxReconnectAttempts})`);
          setTimeout(attemptConnect, delay);
          reconnectAttempts++;
        } else {
          setStatus("Failed to reconnect");
        }
      };

      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        setStatus("Error");
      };

      ws.onmessage = (event) => {
        try {
          console.log("Received WebSocket message:", event.data);
          const data = JSON.parse(event.data);
          console.log("Parsed data:", data);
          if (data.type === "scene_update") {
            const scene = data.scene;
            console.log("Scene elements:", scene.elements);
            const excalidrawElements = mapToExcalidraw(scene.elements);
            
            console.log("Updating Excalidraw with elements:", excalidrawElements);
            if (excalidrawAPI && excalidrawAPI.updateScene) {
              excalidrawAPI.updateScene({
                elements: excalidrawElements,
                appState: {},
              });
              console.log("Scene updated successfully");
            } else {
              console.log("Excalidraw API not ready, saving pending scene");
              setPendingScene({ elements: excalidrawElements });
            }
          }
        } catch (e) {
          console.error("Failed to parse message", e);
        }
      };
    };

    attemptConnect();
  };

  useEffect(() => {
    connectWs();
    return () => wsRef.current?.close();
  }, [excalidrawAPI]);

    useEffect(() => {
    if (excalidrawAPI && pendingScene && excalidrawAPI.updateScene) {
      try {
        excalidrawAPI.updateScene({ elements: pendingScene.elements, appState: {} });
        console.log('Applied pending scene to Excalidraw');
        setPendingScene(null);
      } catch (e) {
        console.error('Failed to apply pending scene', e);
      }
    }
  }, [excalidrawAPI, pendingScene]);

  return (
    <div style={{ height: "100%", display: "flex", flexDirection: "column" }}>
      <div style={{ 
        padding: "10px 20px", 
        borderBottom: "1px solid #ddd", 
        display: "flex", 
        justifyContent: "space-between",
        alignItems: "center",
        backgroundColor: "#f5f5f5"
      }}>
        <h1 style={{ margin: 0, fontSize: "1.2rem" }}>Excalidraw MCP Playground</h1>
        <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
          <span style={{ 
            color: status === "Connected" ? "green" : "red", 
            fontWeight: "bold" 
          }}>
            ● {status}
          </span>
          <button onClick={connectWs}>Reconnect</button>
        </div>
      </div>

      <div style={{ flex: 1, position: "relative" }}>
        <Excalidraw 
          excalidrawAPI={(api) => setExcalidrawAPI(api)}
          initialData={{ elements: [], appState: { viewBackgroundColor: "#ffffff" } }}
        />
      </div>
    </div>
  );
}

export default App;