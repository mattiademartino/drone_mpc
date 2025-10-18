import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import pandas as pd
import os

# Carica solo i dati di posizione
try:
    p = pd.read_csv(os.path.expanduser('~/drone/drone_mpc/drone_state.csv'), header=None).values
    print(f"Dati caricati: {p.shape[0]} campioni, {p.shape[1]} dimensioni")
except FileNotFoundError as e:
    print(f"Errore: File non trovato - {e}")
    exit()

# ============== FIGURA 1: Traiettoria 3D ==============
fig1 = plt.figure(figsize=(10, 8))
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot(p[:, 0], p[:, 1], p[:, 2], 'b-', linewidth=2, label='Traiettoria')
ax1.scatter(p[0, 0], p[0, 1], p[0, 2], c='g', s=100, marker='o', label='Start')
ax1.scatter(p[-1, 0], p[-1, 1], p[-1, 2], c='r', s=100, marker='x', label='End')
ax1.set_xlabel('X (m)')
ax1.set_ylabel('Y (m)')
ax1.set_zlabel('Z (m)')
ax1.set_title('Traiettoria 3D del Drone')
ax1.legend()
ax1.grid(True)

# ============== FIGURA 2: Posizione (componenti) ==============
fig2, axes2 = plt.subplots(3, 1, figsize=(12, 8))
fig2.suptitle('Posizione del Drone', fontsize=14, fontweight='bold')

axes2[0].plot(p[:, 0], 'b-', linewidth=1.5)
axes2[0].set_ylabel('X (m)')
axes2[0].set_title('Posizione X')
axes2[0].grid(True)

axes2[1].plot(p[:, 1], 'g-', linewidth=1.5)
axes2[1].set_ylabel('Y (m)')
axes2[1].set_title('Posizione Y')
axes2[1].grid(True)

axes2[2].plot(p[:, 2], 'r-', linewidth=1.5)
axes2[2].set_ylabel('Z (m)')
axes2[2].set_xlabel('Campioni')
axes2[2].set_title('Posizione Z')
axes2[2].grid(True)

plt.tight_layout()

# ============== ANIMAZIONE 3D ==============
fig3 = plt.figure(figsize=(10, 8))
ax3 = fig3.add_subplot(111, projection='3d')

def update_animation(frame):
    ax3.clear()
    # Mostra la traiettoria fino al frame corrente
    ax3.plot(p[:frame+1, 0], p[:frame+1, 1], p[:frame+1, 2], 'b-', linewidth=2, alpha=0.6)
    
    # Mostra il drone nella posizione corrente
    pos = p[frame]
    ax3.scatter(pos[0], pos[1], pos[2], c='r', s=150, marker='o')
    
    # Mostra gli ultimi N punti come trail
    trail_length = min(20, frame)
    if trail_length > 0:
        ax3.scatter(p[frame-trail_length:frame, 0], 
                   p[frame-trail_length:frame, 1], 
                   p[frame-trail_length:frame, 2], 
                   c='orange', s=30, alpha=0.5)
    
    ax3.set_xlabel('X (m)')
    ax3.set_ylabel('Y (m)')
    ax3.set_zlabel('Z (m)')
    ax3.set_title(f'Animazione Drone - Frame {frame+1}/{len(p)}')
    
    # Mantieni i limiti degli assi costanti
    margin = 0.5
    ax3.set_xlim([p[:, 0].min()-margin, p[:, 0].max()+margin])
    ax3.set_ylim([p[:, 1].min()-margin, p[:, 1].max()+margin])
    ax3.set_zlim([p[:, 2].min()-margin, p[:, 2].max()+margin])
    ax3.grid(True)

# Crea animazione (decommentare per vedere l'animazione)
anim = FuncAnimation(fig3, update_animation, frames=len(p), interval=50, repeat=True)

print("\n=== Statistiche Traiettoria ===")
print(f"Numero di campioni: {len(p)}")
print(f"Posizione iniziale: [{p[0,0]:.3f}, {p[0,1]:.3f}, {p[0,2]:.3f}]")
print(f"Posizione finale:   [{p[-1,0]:.3f}, {p[-1,1]:.3f}, {p[-1,2]:.3f}]")
print(f"Distanza percorsa:  {np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1)):.3f} m")

plt.show()
