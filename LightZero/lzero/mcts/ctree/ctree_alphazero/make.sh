"""
This script compiles the ctree_alphazero project. The compiled files are stored in the "build" directory.

In summary, this script automates the process of creating a new build directory, navigating into it,
running cmake to generate build files suitable for the arm64 architecture, and running make to compile the project.
"""

# Navigate to the project directory
cd /Users/<your_user_name>/code/LightZero/lzero/mcts/ctree/ctree_alphazero/

# Create a new directory named "build." The build directory is where the compiled files will be stored.
mkdir build

# Navigate into the "build" directory
cd build

# Run cmake on the parent directory. The ".." refers to the parent directory of the current directory.
# The -DCMAKE_OSX_ARCHITECTURES="arm64" flag specifies that the generated build files should be suitable for the arm64 architecture.
cmake .. -DCMAKE_OSX_ARCHITECTURES="arm64"

# Run the "make" command. This command uses the files generated by cmake to compile the project.
make