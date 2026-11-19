#!/bin/sh
set -eu

GKI_ROOT=$(pwd)
NyaSU_REPO="https://github.com/xingguangcuican6666/NyaSU.git"

display_usage() {
    echo "Usage: $0 [--cleanup | <commit-or-tag>]"
    echo "  --cleanup:              Cleans up previous modifications made by the script."
    echo "  <commit-or-tag>:        Sets up the NyaSU source at this exact ref."
    echo "  -h, --help:             Displays this usage information."
    echo "  (no args):              Sets up the NyaSU source at the default branch tip."
}

initialize_variables() {
    if [ -d "$GKI_ROOT/common/drivers" ]; then
        DRIVER_DIR="$GKI_ROOT/common/drivers"
    elif [ -d "$GKI_ROOT/drivers" ]; then
        DRIVER_DIR="$GKI_ROOT/drivers"
    else
        echo '[ERROR] "drivers/" directory not found.' >&2
        exit 127
    fi

    DRIVER_MAKEFILE=$DRIVER_DIR/Makefile
    DRIVER_KCONFIG=$DRIVER_DIR/Kconfig
}

perform_cleanup() {
    echo "[+] Cleaning up..."
    if [ -L "$DRIVER_DIR/kernelsu" ]; then
        rm "$DRIVER_DIR/kernelsu"
    fi
    if [ -f "$DRIVER_MAKEFILE" ]; then
        sed -i '\|^obj-$(CONFIG_KSU) += kernelsu/$|d' "$DRIVER_MAKEFILE"
    fi
    if [ -f "$DRIVER_KCONFIG" ]; then
        sed -i '\|^source "drivers/kernelsu/Kconfig"$|d' "$DRIVER_KCONFIG"
    fi
    if [ -d "$GKI_ROOT/KernelSU" ]; then
        rm -rf "$GKI_ROOT/KernelSU"
    fi
    echo "[-] Cleanup complete."
}

setup_nyasu() {
    requested_ref=${1-}
    if [ ! -d "$GKI_ROOT/KernelSU/.git" ]; then
        if [ -e "$GKI_ROOT/KernelSU" ]; then
            echo "[ERROR] $GKI_ROOT/KernelSU exists but is not a Git checkout." >&2
            exit 1
        fi
        git clone "$NyaSU_REPO" "$GKI_ROOT/KernelSU"
    fi

    if [ -n "$requested_ref" ]; then
        git -C "$GKI_ROOT/KernelSU" fetch --tags origin
        if ! git -C "$GKI_ROOT/KernelSU" rev-parse --verify "$requested_ref^{commit}" >/dev/null 2>&1; then
            git -C "$GKI_ROOT/KernelSU" fetch origin "$requested_ref"
        fi
        if ! git -C "$GKI_ROOT/KernelSU" rev-parse --verify "$requested_ref^{commit}" >/dev/null 2>&1; then
            echo "[ERROR] Requested NyaSU ref does not resolve to a commit: $requested_ref" >&2
            exit 1
        fi
        git -C "$GKI_ROOT/KernelSU" checkout --detach "$requested_ref"
    else
        git -C "$GKI_ROOT/KernelSU" remote update --prune
        default_branch=$(git -C "$GKI_ROOT/KernelSU" symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true)
        if [ -z "$default_branch" ]; then
            default_branch=$(git -C "$GKI_ROOT/KernelSU" ls-remote --symref origin HEAD | awk '$1 == "ref:" {sub("refs/heads/", "", $2); print $2; exit}')
        fi
        if [ -z "$default_branch" ]; then
            echo "[ERROR] Cannot determine NyaSU default branch." >&2
            exit 1
        fi
        git -C "$GKI_ROOT/KernelSU" fetch origin "$default_branch"
        git -C "$GKI_ROOT/KernelSU" checkout --detach FETCH_HEAD
    fi

    if [ ! -f "$GKI_ROOT/KernelSU/kernel/Kbuild" ] || [ ! -f "$GKI_ROOT/KernelSU/kernel/Kconfig" ]; then
        echo "[ERROR] Requested ref is missing kernel/Kbuild or kernel/Kconfig." >&2
        exit 1
    fi

    ln -sf "$(realpath --relative-to="$DRIVER_DIR" "$GKI_ROOT/KernelSU/kernel")" "$DRIVER_DIR/kernelsu"
    grep -qF 'obj-$(CONFIG_KSU) += kernelsu/' "$DRIVER_MAKEFILE" || printf '\nobj-$(CONFIG_KSU) += kernelsu/\n' >> "$DRIVER_MAKEFILE"
    grep -qF 'source "drivers/kernelsu/Kconfig"' "$DRIVER_KCONFIG" || sed -i '/endmenu/i\source "drivers/kernelsu/Kconfig"' "$DRIVER_KCONFIG"
    echo "[+] NyaSU set up at $(git -C "$GKI_ROOT/KernelSU" rev-parse HEAD)."
}

if [ "$#" -eq 1 ] && { [ "$1" = "-h" ] || [ "$1" = "--help" ]; }; then
    display_usage
elif [ "$#" -eq 1 ] && [ "$1" = "--cleanup" ]; then
    initialize_variables
    perform_cleanup
elif [ "$#" -le 1 ]; then
    initialize_variables
    setup_nyasu "${1-}"
else
    display_usage >&2
    exit 2
fi
