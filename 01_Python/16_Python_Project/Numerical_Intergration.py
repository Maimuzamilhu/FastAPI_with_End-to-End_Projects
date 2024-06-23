import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


def midpoint_rule(f, a, b, n):
    dx = (b - a) / n
    x = np.linspace(a + dx / 2, b - dx / 2, n)
    return dx * np.sum(f(x))


def f(x):
    return x ** 2


def main():
    st.title("Numerical Integration using Midpoint Rule")

    st.sidebar.header("Input Parameters")
    a = st.sidebar.number_input("Lower bound (a)", value=0.0)
    b = st.sidebar.number_input("Upper bound (b)", value=1.0)
    n = st.sidebar.number_input("Number of subintervals", min_value=1, value=4)

    function_str = st.sidebar.text_input("Enter function (use 'x' as variable)", value="x**2")

    try:
        f = lambda x: eval(function_str)
    except:
        st.error("Invalid function. Please enter a valid Python expression.")
        return

    result = midpoint_rule(f, a, b, n)
    actual = (b ** 3 - a ** 3) / 3  # Actual value for x^2

    st.write(f"Estimated value: {result}")
    st.write(f"Actual value: {actual}")
    st.write(f"Error: {abs(actual - result)}")

    # Visualization
    x = np.linspace(a, b, 200)
    y = f(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'b-', label='f(x)')

    # Plot rectangles
    dx = (b - a) / n
    for i in range(n):
        x_left = a + i * dx
        x_mid = x_left + dx / 2
        y_mid = f(x_mid)
        ax.add_patch(plt.Rectangle((x_left, 0), dx, y_mid, fill=False, edgecolor='r'))


    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.set_title('Midpoint Rule Visualization')

    st.pyplot(fig)


if __name__ == "__main__":
    main()