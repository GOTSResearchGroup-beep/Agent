// Script de prueba para verificar si nut-js puede controlar el mouse
const { mouse, Point, keyboard } = require('@nut-tree-fork/nut-js');

async function testMouse() {
  try {
    console.log('Iniciando test del mouse...');

    // Obtener posición actual
    const currentPos = await mouse.getPosition();
    console.log('Posición actual:', currentPos);

    // Esperar 2 segundos
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Mover el mouse al centro de la pantalla (aprox)
    console.log('Moviendo mouse al centro...');
    await mouse.setPosition(new Point(640, 360));

    await new Promise(resolve => setTimeout(resolve, 1000));

    // Hacer un clic izquierdo
    console.log('Haciendo clic izquierdo...');
    await mouse.leftClick();

    await new Promise(resolve => setTimeout(resolve, 1000));

    // Escribir texto
    console.log('Escribiendo texto...');
    await keyboard.type('Hola mundo');

    console.log('Test completado exitosamente!');

  } catch (error) {
    console.error('Error durante el test:', error);
  }
}

testMouse();
