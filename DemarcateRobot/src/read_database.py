
from app_config import *
def read_infrainit_data(robot,arg):
    try:
        sqlHandle = sqlite3.connect(DATABASE_PATH)
        sqlInterface = sqlHandle.cursor()
        sql = 'SELECT infra_ultra FROM RobotCalibration WHERE robot_id = "%s" ' % (robot.robot_id)    
        RobotDB_Interface.execute(sql)
        ret = RobotDB_Interface.fetchall()
        if len(ret)==0:
            print 'not find infra_ultra data'
            return -1
        else:
            try:
                if ret['flag']==2:
                    infrainit_data=ret['data'][1]
                    print 'infrainit_data=',infrainit_data
                    return infrainit_data
                else:
                    print 'infra_ultra not init success'
                    return -1
            except:
                print 'read infra_ultra data error,please check the database!'
                return -1
    except:
        print 'read infra_ultra data error,please check the database!'

                    
