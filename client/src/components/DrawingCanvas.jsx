import { useRef, useEffect, useState, forwardRef, useImperativeHandle } from 'react';

const DrawingCanvas = forwardRef(({ onSave }, ref) => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [context, setContext] = useState(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = 200;
    canvas.height = 300;
    
    // Set initial canvas state
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    setContext(ctx);
  }, []);

  const startDrawing = (e) => {
    setIsDrawing(true);
    const { offsetX, offsetY } = getCoordinates(e);
    context.beginPath();
    context.moveTo(offsetX, offsetY);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const { offsetX, offsetY } = getCoordinates(e);
    context.lineTo(offsetX, offsetY);
    context.stroke();
  };

  const stopDrawing = () => {
    setIsDrawing(false);
  };

  const getCoordinates = (e) => {
    let offsetX, offsetY;
    if (e.type.startsWith('touch')) {
      const rect = canvasRef.current.getBoundingClientRect();
      const touch = e.touches[0];
      offsetX = touch.clientX - rect.left;
      offsetY = touch.clientY - rect.top;
    } else {
      offsetX = e.nativeEvent.offsetX;
      offsetY = e.nativeEvent.offsetY;
    }
    return { offsetX, offsetY };
  };

  const clearCanvas = () => {
    if (context) {
      context.fillStyle = 'white';
      context.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  };

  useImperativeHandle(ref, () => ({
    clear: clearCanvas
  }));

  const saveDrawing = () => {
    if (canvasRef.current) {
      const imageData = canvasRef.current.toDataURL('image/png');
      onSave(imageData);
    }
  };

  return (
    <div className="drawing-canvas-container">
      <canvas
        ref={canvasRef}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseOut={stopDrawing}
        onTouchStart={startDrawing}
        onTouchMove={draw}
        onTouchEnd={stopDrawing}
        style={{
          border: '1px solid #000',
          touchAction: 'none'
        }}
      />
      <div className="canvas-controls">
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={saveDrawing}>Save</button>
      </div>
    </div>
  );
});

DrawingCanvas.displayName = 'DrawingCanvas';

export default DrawingCanvas;
