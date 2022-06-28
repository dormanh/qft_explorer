from computations import compute_valid_Ns, exp2int


N_QUBITS = 6
N_STATES = exp2int(N_QUBITS)
VALID_NS = compute_valid_Ns(N_STATES)
INITIAL_N = 35

main_title = "Explore the quantum Fourier transform!"
vertical_margin = dict(marginTop=50, marginBottom=50)
horizontal_margin = dict(marginLeft=200, marginRight=200)
font_style = dict(fontSize=20, fontFamily="helvetica")
subtitle_style = dict(fontSize=16, fontWeight="bold")
paragraph_style = dict(
    textAlign="justify",
    fontSize=14,
    fontWeight="normal",
)
