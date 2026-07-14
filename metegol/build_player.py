import numpy as np, trimesh, os
from trimesh.creation import box, cylinder, capsule
from trimesh.transformations import rotation_matrix as R

# ============ PARAMETROS (mm) ============
ROD_D      = 12.7
ROD_CLEAR  = 0.6
PIN_D      = 2.6
rod_hole_d = ROD_D + ROD_CLEAR
rod_z      = 54.0
HEAD_OBJ   = os.path.join(os.path.dirname(__file__), "fuente", "cabeza_escaneada.obj")
BODY_RGBA  = [200,25,25,255]   # rojo clasico

def U(parts): return trimesh.boolean.union(parts, engine='manifold')

# ============ CUERPO estilo metegol clasico ============
parts=[]
# --- pie / base (bloque que en perfil es cuña hacia adelante +Y) ---
foot = box([20,30,14]); foot.apply_translation([0,8,7]); parts.append(foot)
# --- piernas juntas, afinandose hacia abajo (stack que tapa) ---
parts.append(box([24,18,14]).apply_translation([0,0,30]))   # muslos
parts.append(box([19,16,14]).apply_translation([0,0,18]))   # pantorrillas
parts.append(box([16,15,10]).apply_translation([0,1,10]))   # tobillos
# --- cadera / torso (afinado en cintura, ancho en hombros) ---
parts.append(box([24,18,16]).apply_translation([0,0,42]))   # cintura
parts.append(box([30,18,18]).apply_translation([0,0,53]))   # pecho
parts.append(box([32,17,10]).apply_translation([0,0,61]))   # hombros
# hombros redondeados (capsula horizontal)
sh=capsule(height=28,radius=6.5); sh.apply_transform(R(np.pi/2,[0,1,0])); sh.apply_translation([0,1,62]); parts.append(sh)
# leve pecho adelante
chest=trimesh.creation.icosphere(subdivisions=3,radius=7); chest.apply_scale([1.5,0.7,0.9]); chest.apply_translation([0,7,49]); parts.append(chest)
# --- brazos: capsulas finas pegadas a los costados ---
for s in (-1,1):
    arm=capsule(height=24,radius=4.5)
    arm.apply_transform(R(np.deg2rad(5)*s,[0,1,0]))
    arm.apply_translation([s*14.5, 1, 50]); parts.append(arm)
# --- cuello corto y grueso ---
parts.append(cylinder(radius=7.0,height=18,sections=32).apply_translation([0,1,66]))

body=U(parts)
# suavizado para look moldeado (redondea aristas de los primitivos)
trimesh.smoothing.filter_taubin(body, iterations=12)
body=U([body])  # re-normalizar

# --- agujeros (despues de suavizar, quedan limpios) ---
rod=cylinder(radius=rod_hole_d/2,height=80,sections=64).apply_transform(R(np.pi/2,[0,1,0])).apply_translation([0,1,rod_z])
pin=cylinder(radius=PIN_D/2,height=70,sections=32).apply_transform(R(np.pi/2,[1,0,0])).apply_translation([0,1,rod_z])
body=trimesh.boolean.difference([body,rod,pin],engine='manifold')
body.visual.vertex_colors=np.tile(BODY_RGBA,(len(body.vertices),1)).astype(np.uint8)
print("BODY watertight:",body.is_watertight,"shoulders_z_top:",round(body.bounds[1][2],1))

# ============ CABEZA nitida y estanca ============
h=trimesh.load(HEAD_OBJ, process=True)
V=h.vertices.copy(); h.vertices=np.column_stack([V[:,0],V[:,2],V[:,1]])  # up=Z, forward=Y
# color por vertice desde el obj (r g b en las lineas v)
verts=[]; cols=[]
with open(HEAD_OBJ) as f:
    for l in f:
        if l.startswith('v '):
            p=l.split(); verts.append([float(p[1]),float(p[3]),float(p[2])]); cols.append([float(p[4]),float(p[5]),float(p[6])])
verts=np.array(verts); cols=np.array(cols)
# mapear color a los vertices procesados por vecino mas cercano
from scipy.spatial import cKDTree
tree=cKDTree(verts); _,idx=tree.query(h.vertices)
h.visual.vertex_colors=(np.clip(cols[idx],0,1)*255).astype(np.uint8)
trimesh.repair.fill_holes(h); trimesh.repair.fix_normals(h)
# recorte con tapa -> estanco, cara intacta
zmin,zmax=h.bounds[0][2],h.bounds[1][2]; H=zmax-zmin
cutf, chinf, HEAD_MM, CHIN_Z = 0.22, 0.40, 26.0, 74.0
cut=zmin+cutf*H
head=h.slice_plane(plane_origin=[0,0,cut],plane_normal=[0,0,1],cap=True)
# escala: la altura menton->coronilla = HEAD_MM
scale=HEAD_MM/((1.0-chinf)*H); head.apply_scale(scale)
head.apply_translation([-head.centroid[0], -1.5-head.centroid[1], -head.bounds[0][2]])  # centrar xy (leve atras), base a 0
chin_local=(chinf-cutf)*H*scale
head.apply_translation([0,0, CHIN_Z-chin_local])   # menton a z=CHIN_Z (arriba de hombros ~66)
print("HEAD watertight:",head.is_watertight,"faces",len(head.faces),"top_z:",round(head.bounds[1][2],1))

# ============ COMBINAR ============
try:
    solid=trimesh.boolean.union([body,head],engine='manifold')
    print("UNION watertight:",solid.is_watertight,"faces",len(solid.faces))
    ok=solid.is_watertight
except Exception as e:
    print("union fallo:",e); ok=False
if not ok:
    solid=trimesh.util.concatenate([body,head])  # multibody (el slicer lo une)
    print("uso multibody watertight-parts")

final=trimesh.util.concatenate([body,head])  # a color

# ============ EXPORT ============
out=os.path.join(os.path.dirname(__file__),"salida"); os.makedirs(out,exist_ok=True)
solid.export(out+"/jugador_metegol_prueba.stl"); solid.export(out+"/jugador_metegol_prueba.3mf"); final.export(out+"/jugador_metegol_prueba.glb")
dims=final.bounds[1]-final.bounds[0]
print("Alto x Ancho x Prof:",np.round([dims[2],dims[0],dims[1]],1))
print("OK")
