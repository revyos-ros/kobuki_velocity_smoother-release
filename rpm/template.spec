%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/iron/.*$
%global __requires_exclude_from ^/opt/ros/iron/.*$

Name:           ros-iron-kobuki-velocity-smoother
Version:        0.15.0
Release:        3%{?dist}%{?release_suffix}
Summary:        ROS kobuki_velocity_smoother package

License:        BSD
URL:            https://index.ros.org/p/kobuki_velocity_smoother/github-kobuki-base-velocity_smoother/
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-iron-geometry-msgs
Requires:       ros-iron-nav-msgs
Requires:       ros-iron-rcl-interfaces
Requires:       ros-iron-rclcpp
Requires:       ros-iron-rclcpp-components
Requires:       ros-iron-ros-workspace
BuildRequires:  ros-iron-ament-cmake-ros
BuildRequires:  ros-iron-ecl-build
BuildRequires:  ros-iron-geometry-msgs
BuildRequires:  ros-iron-nav-msgs
BuildRequires:  ros-iron-rcl-interfaces
BuildRequires:  ros-iron-rclcpp
BuildRequires:  ros-iron-rclcpp-components
BuildRequires:  ros-iron-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  python%{python3_pkgversion}-matplotlib
BuildRequires:  ros-iron-ament-cmake-cppcheck
BuildRequires:  ros-iron-ament-cmake-cpplint
BuildRequires:  ros-iron-ament-cmake-flake8
BuildRequires:  ros-iron-ament-cmake-lint-cmake
BuildRequires:  ros-iron-ament-cmake-pep257
BuildRequires:  ros-iron-ament-cmake-uncrustify
BuildRequires:  ros-iron-ament-cmake-xmllint
BuildRequires:  ros-iron-ament-lint-auto
BuildRequires:  ros-iron-launch-testing
BuildRequires:  ros-iron-launch-testing-ament-cmake
BuildRequires:  ros-iron-launch-testing-ros
BuildRequires:  ros-iron-ros2test
%endif

%description
Bound incoming velocity messages according to robot velocity and acceleration
limits.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/iron" \
    -DAMENT_PREFIX_PATH="/opt/ros/iron" \
    -DCMAKE_PREFIX_PATH="/opt/ros/iron" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/iron/setup.sh" ]; then . "/opt/ros/iron/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/iron

%changelog
* Thu Apr 20 2023 Jihoon Lee <jihoonl@yujinrobot.com> - 0.15.0-3
- Autogenerated by Bloom

* Tue Mar 21 2023 Jihoon Lee <jihoonl@yujinrobot.com> - 0.15.0-2
- Autogenerated by Bloom

