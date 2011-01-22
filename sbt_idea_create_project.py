#!/usr/bin/env python

"""Create a skeleton project with SBT and the SBT Idea plugin"""

import argparse
import os
from string import Template

DIRECTORIES = [ 'src/main/scala',
                'src/test/scala',
                'project/build',
                'project/plugins' ]

BUILD_PROPERTIES_T = '''project.organization=$group
project.name=$artifact
sbt.version=0.7.4
project.version=$version
build.scala.versions=2.8.1
project.initialize=false

'''

PLUGINS_SCALA = '''import sbt._

class Plugins(info: ProjectInfo) extends PluginDefinition(info) {
  val sbtIdeaRepo = "sbt-idea-repo" at "http://mpeltonen.github.com/maven/"
  val sbtIdea = "com.github.mpeltonen" % "sbt-idea-plugin" % "0.2.0"
}

'''

PROJECT_SCALA_T = '''import sbt._

class ${proj}Project(info: ProjectInfo) extends DefaultProject(info) with IdeaProject {
  override def repositories = Set(ScalaToolsSnapshots)

  val specs = "org.scala-tools.testing" %% "specs" % "1.6.6" % "test"
}

'''

MAIN_SCALA_T = '''package $group

object Main {

  def main(args: Array[String]) = {

  }
}


'''

SPEC_SCALA_T = '''package $group

import org.specs.Specification

class ${proj}Spec extends Specification {

}

'''

def main():
    parser = argparse.ArgumentParser(description=
                                     'Create a template Scala project.')
    parser.add_argument('group', type=str)
    parser.add_argument('artifact', type=str)
    parser.add_argument('version', type=str, default='0.1.0', nargs='?')
    args = parser.parse_args()
    
    group = args.group
    artifact = args.artifact
    version = args.version
    
    # Create all the directory
    for directory in DIRECTORIES:
        os.makedirs(directory)

    # Create the main dir for the package
    main_path = 'src/main/scala/' + '/'.join(group.split('.'))
    os.makedirs(main_path)
    
    # Create the test dir for the package
    spec_path = 'src/test/scala/' + '/'.join(group.split('.'))
    os.makedirs(spec_path)

    proj = artifact.capitalize()
    
    # Create build.properties
    build_properties = Template(BUILD_PROPERTIES_T).substitute(
        group=group,
        artifact=artifact,
        version=version)

    # Other files
    project_scala = Template(PROJECT_SCALA_T).substitute(proj=proj)
    main_scala = Template(MAIN_SCALA_T).substitute(group=group)
    spec_scala = Template(SPEC_SCALA_T).substitute(group=group, proj=proj)

    build_properties_file = open('project/build.properties', 'w')
    build_properties_file.write(build_properties)
    build_properties_file.close()

    plugins_scala_file = open('project/plugins/Plugins.scala', 'w')
    plugins_scala_file.write(PLUGINS_SCALA)
    plugins_scala_file.close()

    project_scala_file = open('project/build/' + proj + 'Project.scala', 'w')
    project_scala_file.write(project_scala)
    project_scala_file.close()

    main_scala_file = open(main_path + '/Main.scala', 'w')
    main_scala_file.write(main_scala)
    main_scala_file.close()

    spec_scala_file = open(spec_path + '/' + proj + 'Spec.scala', 'w')
    spec_scala_file.write(spec_scala)
    spec_scala_file.close()

if __name__ == '__main__':
    main()



    

    
    


                
