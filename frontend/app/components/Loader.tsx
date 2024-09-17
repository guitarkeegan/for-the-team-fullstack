export default function Loader() {
    return (
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <circle cx="50" cy="50" r="45" fill="#1D428A" stroke="#C8102E" stroke-width="5"/>

  <path d="M50,5 A45,45 0 1,1 50,95" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <path d="M5,50 A45,45 0 0,1 95,50" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <path d="M23,20 Q50,50 23,80" fill="none" stroke="#FFFFFF" stroke-width="3"/>
  <path d="M77,20 Q50,50 77,80" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <animateTransform
    attributeName="transform"
    type="rotate"
    from="0 50 50"
    to="360 50 50"
    dur="1s"
    repeatCount="indefinite"/>
        </svg>
    );
}
