import numpy as np
import trimesh
from trimesh.creation import box, cylinder

# ================== PARAMETROS (mm) - cambiar cuando haya metegol real ==========
ROD_D      = 12.7     # diametro de la varilla (1/2"). CAMBIAR al valor real.
ROD_CLEAR  = 0.6      # holgura para que entre y gire
PIN_D      = 2.6      # diametro del agujero para pasador
rod_hole_d = ROD_D + ROD_CLEAR

import os
HEAD_OBJ = os.path.join(os.path.dirname(__file__), "fuente", "cabeza_escaneada.obj")

# ================== CARGA CABEZA ==================
verts=[]; cols=[]; faces=[]
with open(HEAD_OBJ) as f:
    for l in f:
        if l.startswith('v '):
            p=l.split()
            verts.append([float(p[1]),float(p[2]),float(p[3])])
            cols.append([float(p[4]),float(p[5]),float(p[6])] if len(p)>=7 else [0.7,0.6,0.55])
        elif l.startswith('f '):
            p=l.split()[1:]
            idx=[int(x.split('/')[0])-1 for x in p]
            for i in range(1,len(idx)-1):
                faces.append([idx[0],idx[i],idx[i+1]])
Vh=np.array(verts); Ch=np.array(cols); Fh=np.array(faces)

# axis: obj Y-up, face +Z. Queremos body Z-up, forward +Y.  (X,Y,Z)=(x, z, y)
Vh = np.column_stack([Vh[:,0], Vh[:,2], Vh[:,1]])

# recortar hombros: quedarnos con la parte de arriba (cabeza+cuello)
zmin,zmax = Vh[:,2].min(), Vh[:,2].max()
H = zmax-zmin
cut = zmin + 0.34*H          # corta hombros
keep = Vh[:,2] > cut
# remapear caras que quedan completas
remap = -np.ones(len(Vh),int)
remap[keep] = np.arange(keep.sum())
Vh2 = Vh[keep]; Ch2 = Ch[keep]
fmask = keep[Fh].all(axis=1)
Fh2 = remap[Fh[fmask]]

head = trimesh.Trimesh(vertices=Vh2, faces=Fh2, vertex_colors=(np.clip(Ch2,0,1)*255).astype(np.uint8), process=True)

# escalar cabeza a altura deseada
target_head_h = 26.0
sc = target_head_h / (head.bounds[1][2]-head.bounds[0][2])
head.apply_scale(sc)
# centrar en x,y ; base al origen
head.apply_translation([-head.centroid[0], -head.centroid[1], -head.bounds[0][2]])

# ================== CUERPO ==================
parts=[]
# piernas / cadera
legs = box([26,24,36]); legs.apply_translation([0,0,18]); parts.append(legs)
# pie (patada) hacia adelante +Y
foot = box([18,26,12]); foot.apply_translation([0,17,6]); parts.append(foot)
# torso
torso = box([34,20,40]); torso.apply_translation([0,0,56]); parts.append(torso)
# hombros redondeados (cilindro horizontal arriba del torso)
sh = cylinder(radius=10, height=34, sections=32);
sh.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
sh.apply_translation([0,0,74]); parts.append(sh)
# brazos pegados a los costados
for s in (-1,1):
    arm = box([7,13,32]); arm.apply_translation([s*19.5,0,54]); parts.append(arm)
# cuello
neck = cylinder(radius=6.5, height=10, sections=24); neck.apply_translation([0,0,80]); parts.append(neck)

body = trimesh.boolean.union(parts, engine='manifold')

# ================== AGUJEROS ==================
rod_z = 50.0
rod = cylinder(radius=rod_hole_d/2, height=80, sections=48)
rod.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))  # eje X
rod.apply_translation([0,0,rod_z])
pin = cylinder(radius=PIN_D/2, height=60, sections=24)
pin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))  # eje Y
pin.apply_translation([0,0,rod_z])

body = trimesh.boolean.difference([body, rod, pin], engine='manifold')

# color del cuerpo (camiseta azul)
body.visual.vertex_colors = np.tile([30,60,160,255],(len(body.vertices),1)).astype(np.uint8)

# ================== MONTAR CABEZA ==================
head.apply_translation([0,0, 82.0])  # base de la cabeza a z=82 (cuello visible ~76-84)

# cerrar la base abierta de la cabeza para volverla estanca (watertight)
trimesh.repair.fill_holes(head)
trimesh.repair.fix_normals(head)
print("head watertight tras fill:", head.is_watertight)

# version a color (para visor/full-color): concatenacion conservando colores
final = trimesh.util.concatenate([body, head])

# solido unico para imprimir (STL): re-mallo por voxeles -> watertight garantizado
combined = trimesh.util.concatenate([body, head])
pitch = 0.5
vg = combined.voxelized(pitch=pitch).fill()
solid = vg.marching_cubes
# el marching_cubes viene en indices de voxel -> re-escalar a mm y alinear
solid.apply_scale(pitch)
solid.apply_translation(combined.bounds[0] - solid.bounds[0])
# suavizado leve (Taubin) para sacar el escalonado del voxel
trimesh.smoothing.filter_taubin(solid, iterations=10)
solid.fix_normals()
print("SOLID(voxel) watertight:", solid.is_watertight, "faces:", len(solid.faces),
      "vol_cm3:", round(solid.volume/1000,1), "alto_mm:", round((solid.bounds[1]-solid.bounds[0])[2],1))

# ================== EXPORT ==================
out_dir=os.path.join(os.path.dirname(__file__), "salida")
os.makedirs(out_dir, exist_ok=True)
solid.export(out_dir+"/jugador_metegol_prueba.stl")          # para imprimir (solido unico)
solid.export(out_dir+"/jugador_metegol_prueba.3mf")          # para imprimir (alternativa)
final.export(out_dir+"/jugador_metegol_prueba.glb")          # con color (visor)

print("SOLID watertight:", solid.is_watertight, "vol_mm3:", round(solid.volume,1))
print("BODY watertight:", body.is_watertight, "vol_mm3:", round(body.volume,1))
print("FINAL bounds (mm):"); print(np.round(final.bounds,1))
dims = final.bounds[1]-final.bounds[0]
print("Alto x Ancho x Prof (mm):", np.round([dims[2],dims[0],dims[1]],1))
print("Rod hole diam:", rod_hole_d, " a altura z=",rod_z)
np.save("/tmp/final_v.npy", final.vertices)
np.save("/tmp/final_c.npy", final.visual.vertex_colors[:,:3])
np.save("/tmp/final_f.npy", final.faces)
print("OK")
