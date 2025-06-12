import React from 'react';
import Particles from 'react-tsparticles';
import { loadFull } from 'tsparticles'; // 3.x engine

export default function ParticlesBg() {
  const particlesInit = React.useCallback(async (engine) => {
    await loadFull(engine);
  }, []);

  const options = React.useMemo(
    () => ({
      fullScreen: { enable: false },
      fpsLimit: 60,
      background: { color: 'transparent' },
      particles: {
        number: { value: 40 },
        color: { value: ['#43c06d', '#29984a', '#ffffff'] },
        shape: { type: 'circle' },
        opacity: { value: 0.3 },
        size: { value: { min: 1, max: 4 } },
        move: { enable: true, speed: 1.2, direction: 'none', outModes: 'bounce' },
      },
      interactivity: {
        events: { onHover: { enable: true, mode: 'repulse' }, resize: true },
        modes: { repulse: { distance: 80 } },
      },
      detectRetina: true,
    }),
    []
  );

  return (
    <Particles
      id="tsparticles"
      options={options}
      init={particlesInit}
      style={{ position: 'absolute', inset: 0, zIndex: -1 }}
    />
  );
}
