import maya.cmds as cmds

class ButtonWin(object):
    def __init__(self):
        pass
        
    def show(self):
        self.createMyLayout()
        
    def createMyLayout(self):
        if cmds.window('utility', exists = True):
            cmds.deleteUI('utility')

        self.win = cmds.window('utility', widthHeight = (200, 200), title = 'Orient_Joints', resizeToFitChildren=1, sizeable = False)
        self.layout = cmds.columnLayout(parent=self.win)
        cmds.radioButtonGrp("rbgAim", l="Aim Axis:", nrb=3, la3=("X","Y","Z"), sl=1, cw4=(80,40,40,40))
        cmds.radioButtonGrp("rbgUp", l="Up Axis:", nrb=3, la3=("X","Y","Z"), sl=2, cw4=(80,40,40,40))
        cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
        cmds.checkBox("chbReverseAim", l="Reverse AIM")
        cmds.checkBox("chbReverseUp", l="Reverse UP")
        cmds.setParent( '..' )
        cmds.radioButtonGrp("rbgAllOrSelected", l="Operate on:", nrb=2, la2=("Hierarchy","Selected"), sl=1, cw3=(80,80,80))
        cmds.floatFieldGrp("rbgWorldUp", l="World Up: ", nf=3, v1=0.0, v2=1.0, v3=0.0, cw4=(65,50,50,50))
        cmds.rowLayout (cw3 = (50, 280, 40), nc = 4)
        cmds.button("btnXUp", l="X", w=50, h=20, c=worldUpX)
        cmds.button("btnYUp", l="Y", w=50, h=20, c=worldUpY)
        cmds.button("btnZUp", l="Z", w=50, h=20, c=worldUpZ)
        cmds.setParent( '..' )			
        cmds.checkBox("chbGuess", l="Guess Up Direction")
        cmds.button("btnOrientJoints", l="Orient Joints", al="center", h=40, c=self.orientJointsUI, ann="Orient Joints")		
        self.fieldGrp = cmds.floatFieldGrp( numberOfFields=3, label = "joints", v1=0,v2=0,v3=0,cw4=(80,40,40,40))
        cmds.button( label = "Orient", parent=self.layout, command=self.queryPadding )
        self.sacle_j = cmds.floatFieldGrp( numberOfFields=1, label = "scale", v1=0.5 )
        cmds.button( label = "Scale_Joints", parent=self.layout, command=self.scale_joints )
        cmds.separator()
        cmds.iconTextButton("lblCopyright1", l="All Rights Reserved.", w=310, h=20, style="textOnly", c="cmds.showHelp(\"http://www.arthurcurymeirelle.wixsite.com/art3d\", a=1)")
        cmds.showWindow()
        
 
    def queryPadding(self, arg=None):
     padding = cmds.floatFieldGrp(self.fieldGrp, query=True, value1=True)
     padding2 = cmds.floatFieldGrp(self.fieldGrp, query=True,value2=True)
     padding3 = cmds.floatFieldGrp(self.fieldGrp, query=True,value3=True)
     jointlist = cmds.ls(sl=True)
     for eachJointSelected in jointlist:
        rotation = cmds.xform(eachJointSelected, r=1, os=1, ra=[padding, padding2, padding3]) 
        print (rotation)
        jointToOrient = cmds.ls(sl=True)
        cmds.joint(jointToOrient, e=True, zeroScaleOrient=True) 
        cmds.makeIdentity(jointToOrient, apply=True, t=0, r=1, s=0, n=0)
        
    def joints_xyz():
         joint_xyz = cmds.ls(sl=True)
         print (joint_xyz)
         item= 'yzx'
         cmds.joint( joint_xyz, e=True, zso=True, oj= item,sao='zup',ch=True )

    def yzx_up(self, arg=None):
        joint_xyz = cmds.ls(sl=True)
        print (joint_xyz)
        cmds.joint( joint_xyz, e=True, zso=True, oj= 'yzx',sao='zup',ch=True )
        
    def scale_joints(self, arg=None):
        scale = cmds.floatFieldGrp(self.sacle_j, query=True, value1=True)
        cmds.jointDisplayScale( scale )
        
    def orientJointsUI(self,* args):
        aimSelected = cmds.radioButtonGrp("rbgAim", q=True, sl=True)
        upSelected = cmds.radioButtonGrp("rbgUp", q=True, sl=True)

        aimReverse = cmds.checkBox("chbReverseAim", q=True, v=True)
        upReverse = cmds.checkBox("chbReverseUp", q=True, v=True)

        operateOn = cmds.radioButtonGrp("rbgAllOrSelected", q=True, sl=True)

        worldUp = [0,0,0]
        worldUp[0] = cmds.floatFieldGrp("rbgWorldUp", q=True, v1=True)
        worldUp[1] = cmds.floatFieldGrp("rbgWorldUp", q=True, v2=True)
        worldUp[2] = cmds.floatFieldGrp("rbgWorldUp", q=True, v3=True)

        guessUp = cmds.checkBox("chbGuess", q=True, v=True)

        aimAxis = [0,0,0]
        upAxis = [0,0,0]

        if aimReverse == 1:
            aimAxis[aimSelected - 1] = -1
        else:
            aimAxis[aimSelected - 1] = 1

        if upReverse == 1:
            upAxis[upSelected - 1] = -1
        else:
            upAxis[upSelected - 1] = 1

        elemSelected = cmds.ls(typ="joint", sl=True)

        cmds.undoInfo(ock=True)

        if aimSelected == upSelected:
            print("USE: Aim Axis and Up Axis can't be the same.")
        else:
            if elemSelected == None or len(elemSelected) == 0:
                print("USE: Select at least one joint to orient.")
            else:
                if operateOn == 1:
                    #Hierarchy
                    cmds.select(hi=True)
                    jointsToOrient = cmds.ls(typ="joint", sl=True)
                else:
                    #Selected
                    jointsToOrient = cmds.ls(typ="joint", sl=True)

            

                doOrientJoint(jointsToOrient, aimAxis, upAxis, worldUp, guessUp)
                cmds.select(elemSelected, r=True)

        cmds.undoInfo(cck=True)

    
def doOrientJoint(jointsToOrient, aimAxis, upAxis, worldUp, guessUp):
	firstPass = 0
	prevUpVector = [0,0,0]
	for eachJoint in jointsToOrient:
		childJoint = cmds.listRelatives(eachJoint, type="joint", c=True) 
		if childJoint != None:
			if len(childJoint) > 0:

				childNewName = cmds.parent(childJoint, w=True)	#Store the name in case when unparented it changes it's name.

				if guessUp == 0:
					#Not guess Up direction
					
					cmds.delete(cmds.aimConstraint(childNewName[0], eachJoint, w=1, o=(0,0,0), aim=aimAxis, upVector=upAxis, worldUpVector=worldUp, worldUpType="vector"))
					freezeJointOrientation(eachJoint)
					cmds.parent(childNewName, eachJoint)
				else:
					if guessUp == 1:
						#Guess Up direction
						

						parentJoint = cmds.listRelatives(eachJoint, type="joint", p=True) 
						if parentJoint != None :
							if len(parentJoint) > 0:
								posCurrentJoint = cmds.xform(eachJoint, q=True, ws=True, rp=True)
								posParentJoint = cmds.xform(parentJoint, q=True, ws=True, rp=True)
								tolerance = 0.0001

								if (abs(posCurrentJoint[0] - posParentJoint[0]) <= tolerance and abs(posCurrentJoint[1] - posParentJoint[1]) <= tolerance and abs(posCurrentJoint[2] - posParentJoint[2]) <= tolerance):
									aimChild = cmds.listRelatives(childNewName[0], type="joint", c=True) 
									upDirRecalculated = crossProduct(eachJoint, childNewName[0], aimChild[0])
									cmds.delete(cmds.aimConstraint(childNewName[0], eachJoint, w=1, o=(0,0,0), aim=aimAxis, upVector=upAxis, worldUpVector=upDirRecalculated, worldUpType="vector"))
								else:
									upDirRecalculated = crossProduct(parentJoint, eachJoint, childNewName[0])
									cmds.delete(cmds.aimConstraint(childNewName[0], eachJoint, w=1, o=(0,0,0), aim=aimAxis, upVector=upAxis, worldUpVector=upDirRecalculated, worldUpType="vector"))
							else:
								aimChild = cmds.listRelatives(childNewName[0], type="joint", c=True) 
								upDirRecalculated = crossProduct(eachJoint, childNewName[0], aimChild[0])
						else:
							aimChild = cmds.listRelatives(childNewName[0], type="joint", c=True) 
							upDirRecalculated = crossProduct(eachJoint, childNewName[0], aimChild[0])
							cmds.delete(cmds.aimConstraint(childNewName[0], eachJoint, w=1, o=(0,0,0), aim=aimAxis, upVector=upAxis, worldUpVector=upDirRecalculated, worldUpType="vector"))

				



					dotProduct = upDirRecalculated[0] * prevUpVector[0] + upDirRecalculated[1] * prevUpVector[1] + upDirRecalculated[2] * prevUpVector[2]

					#For the next iteration
					prevUpVector = upDirRecalculated

					if firstPass > 0 and  dotProduct <= 0.0:
						#dotProduct
						cmds.xform(eachJoint, r=1, os=1, ra=(aimAxis[0] * 180.0, aimAxis[1] * 180.0, aimAxis[2] * 180.0))
						prevUpVector[0] *= -1
						prevUpVector[1] *= -1
						prevUpVector[2] *= -1
		
					freezeJointOrientation(eachJoint)
					cmds.parent(childNewName, eachJoint)




			else:
				#Child joint. Use the same rotation as the parent.
				if len(childJoint) == 0:
					parentJoint = cmds.listRelatives(eachJoint, type="joint", p=True) 
					if parentJoint != None :
						if len(parentJoint) > 0:
							cmds.delete(cmds.orientConstraint(parentJoint[0], eachJoint, w=1, o=(0,0,0)))
							freezeJointOrientation(eachJoint)
		else:
			#Child joint. Use the same rotation as the parent.
			parentJoint = cmds.listRelatives(eachJoint, type="joint", p=True) 
			if parentJoint != None :
				if len(parentJoint) > 0:
					cmds.delete(cmds.orientConstraint(parentJoint[0], eachJoint, w=1, o=(0,0,0)))
					freezeJointOrientation(eachJoint)			

	

		firstPass += 1
        
        
   
    

def joint_qualquer(self,* args):
    print (actObject)
    cmds.delete(actObject)


def worldUpX(self,* args):
	cmds.floatFieldGrp("rbgWorldUp", e=True, v1=1.0)
	cmds.floatFieldGrp("rbgWorldUp", e=True, v2=0.0)
	cmds.floatFieldGrp("rbgWorldUp", e=True, v3=0.0)
    
    
    
def worldUpY(self,* args):
	cmds.floatFieldGrp("rbgWorldUp", e=True, v1=0.0)
	cmds.floatFieldGrp("rbgWorldUp", e=True, v2=1.0)
	cmds.floatFieldGrp("rbgWorldUp", e=True, v3=0.0)
    
    
def worldUpZ(self,* args):
	cmds.floatFieldGrp("rbgWorldUp", e=True, v1=0.0)
	cmds.floatFieldGrp("rbgWorldUp", e=True, v2=0.0)
	cmds.floatFieldGrp("rbgWorldUp", e=True, v3=1.0)
    





    
    
    
def freezeJointOrientation(jointToOrient):
	cmds.joint(jointToOrient, e=True, zeroScaleOrient=True)
	cmds.makeIdentity(jointToOrient, apply=True, t=0, r=1, s=0, n=0)
    
    
b_cls = ButtonWin()  
b_cls.show()


