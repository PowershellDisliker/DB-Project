import loadingStyles from "./loading.module.css"

function LoadingIcon() {

    return (
        <div className={loadingStyles.spinner} />
    )
}

export default LoadingIcon;