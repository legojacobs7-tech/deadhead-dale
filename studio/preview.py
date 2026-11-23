import sys; sys.path.insert(0, "/home/claude/deadhead-dale/studio")
import bpy, importlib
ep = importlib.import_module(sys.argv[1]); k = int(sys.argv[2]); N = int(sys.argv[3]); frac = float(sys.argv[4])
ep.build(ep.SHOTS[k][1], N)
sc = bpy.context.scene; sc.frame_set(max(1, int(N * frac)))
sc.render.resolution_percentage = 50
sc.render.filepath = f"/home/claude/deadhead-dale/studio/prev/{sys.argv[1]}_{k:02d}.png"
bpy.ops.render.render(write_still=True)
