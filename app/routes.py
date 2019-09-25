from flask import render_template
from flask import Markup
from flask import request
from app import app
from app.AddJointForm import CAddJointForm
import scenebuilder as sb
import FEA
import os
import flask



@app.route('/')
@app.route('/Scene1')
def Scene1():
    Geom = {'X':200,'Y':200,'Z':200}
    return render_template('Scene1.html', Geom=Geom)

@app.route('/Scene2')
def Scene2():
  return render_template('Scene2.html')

@app.route('/Scene3')
def Scene3():
  scene_3 = sb.CScene()
  bodycode = scene_3.body_string

  return render_template('Scene3.html',bodycode=Markup(bodycode))


@app.route('/Menu')
def Menu():
  return render_template('Menu.html')



@app.route('/AddJoint',methods=['GET','POST'])
def AddJoint():
  form = CAddJointForm()
  if form.validate_on_submit():
    #where the event occurs and where I can access data
    print(form.x.data)


  return render_template('AddJoint.html',form=form)

@app.route('/FEA')
def func_FEA():
  inch = 1.
  lb = 1.
  kip = 1000.*lb
  ft = inch*12.
  ksi = kip/(inch**2)
  psi = lb/(inch**2)
  klf = kip/(ft)
  plf = lb/(ft)
  #generate object model dataframe
  om = FEA.StructModel()
  #add nodes
  om.AddNode(0,(0.,0.,0.))
  om.AddNode(1,(0.,10.,0.))
  om.AddNode(2,(10.,10.,0.))
  om.AddNode(3,(10.,0.,0.))

  #add frame members
  # [...] anticipate fucture code to assign material properties to lines which then feed into the stiffness matrix
  om.AddLine(0,(0,1))
  om.AddLine(1,(1,2))
  om.AddLine(2,(2,3))
  #add forces
  om.AddForce(1,(1.*kip,0.*kip,0.*kip*ft))
  om.AddForce(2,(1.*kip,0.*kip,0.*kip*ft))
  #add boundary conditions (x res, y res, rotational res)
  om.AddBoundary(0,(1,1,1))
  om.AddBoundary(3,(1,1,1))

  #generate the basic element stiffness matrix. in future will need to use different ones for different elements
  k_elem = om.GenElemStiff()
  K_Glob_Pure = om.GlobalStiff(k_elem) 
  K = om.mkboundary(K_Glob_Pure,om.getbound())
  d= om.solver(K)
  print(d)

  return "<html><body>" + str(d) + "</body></html>"


@app.route('/index')
def Layout():
  global om
  om = FEA.StructModel()
  return render_template('index.html')


@app.route('/test', methods=['GET','POST'])
def test():
  x=None
  y=None
  z=None
  if request.method == "POST":
    pt_label = request.json['pt_label']
    x=request.json['x']
    y=request.json['y']
    z=request.json['z']
    inch = 1.
    lb = 1.
    kip = 1000.*lb
    ft = inch*12.
    ksi = kip/(inch**2)
    psi = lb/(inch**2)
    klf = kip/(ft)
    plf = lb/(ft)

    #access the global variable
    om.AddNode(pt_label,(x,y,z))
    print(om.node_df.to_json(orient='split'))
  return om.node_df.to_json(orient='split')